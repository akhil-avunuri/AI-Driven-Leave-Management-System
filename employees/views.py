from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from admin_role.models import department, leave
from .models import leaveapplication
from django.contrib import messages
import google.generativeai as genai
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def leave_form(request):
    departments = department.objects.all()
    leaves = leave.objects.all()
    return render(request, 'leave_form.html', {'departments': departments, 'leaves': leaves})

def apply_leave(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id', '').strip()
        employee_name = request.POST.get('employee_name', '').strip()
        department_id = request.POST.get('department_id', '').strip()
        leave_type_id = request.POST.get('leave_id', '').strip()
        leave_description = request.POST.get('leave_description', '').strip()
        from_date = request.POST.get('from_date', '')
        to_date = request.POST.get('to_date', '')

        if not department_id or not leave_type_id:
            messages.error(request, "Please select a valid department and leave type.")
            return redirect('leave_form')  # Redirect back to the form

        if not from_date or not to_date:
            messages.error(request, "Please select valid dates for your leave period.")
            return redirect('leave_form')

        # Validate and fetch Department & LeaveType
        try:
            department_obj = department.objects.get(id=int(department_id))
        except (ValueError, department.DoesNotExist):
            messages.error(request, "Invalid Department selected.")
            return redirect('leave_form')

        try:
            leave_obj = leave.objects.get(id=int(leave_type_id))
        except (ValueError, leave.DoesNotExist):
            messages.error(request, "Invalid Leave Type selected.")
            return redirect('leave_form')

        # Save the leave application
        leave_application_obj = leaveapplication(
            employee_id=employee_id,
            employee_name=employee_name,
            department=department_obj,
            leave_type=leave_obj,
            leave_description=leave_description,
            from_date=from_date,
            to_date=to_date
        )
        leave_application_obj.save()

        messages.success(request, "Leave application submitted successfully.")
        return redirect('leave_form')  # Redirect to the leave form view

    # If not a POST request, redirect to leave form page
    return redirect('leave_form')

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
def get_probability_score(request):
    if request.method == "POST":
        try:
            # Parse request data
            data = json.loads(request.body)
            leave_text = data.get("leave_description", "").strip()

            if not leave_text:
                return JsonResponse({"error": "Leave description is required"}, status=400)

            # Make sure API key is configured
            if not settings.GEMINI_API_KEY:
                return JsonResponse({"error": "AI service not configured", "probability_score": 0.5}, status=200)

            # Generate a probability score based on text length and keywords
            # This is a fallback method when AI is not available
            def calculate_fallback_score(text):
                # Simple scoring algorithm based on text characteristics
                length_score = min(len(text) / 500, 1.0) * 0.3  # Longer text up to 500 chars gets higher score
                
                # Check for positive keywords
                positive_keywords = ['urgent', 'emergency', 'medical', 'family', 'health', 'doctor', 'hospital', 
                                    'sick', 'illness', 'appointment', 'important']
                keyword_score = 0
                for keyword in positive_keywords:
                    if keyword.lower() in text.lower():
                        keyword_score += 0.05
                
                # Cap keyword score
                keyword_score = min(keyword_score, 0.5)
                
                # Total score
                total_score = 0.2 + length_score + keyword_score  # Base score of 0.2
                return min(total_score, 0.95)  # Cap at 0.95
            
            try:
                # Configure the API
                genai.configure(api_key=settings.GEMINI_API_KEY)
                
                # Create a prompt for leave probability evaluation
                prompt = (f"You are evaluating a leave request. Based on the following text, "
                         f"rate how appropriate this leave request is as a single number between 0 and 1, "
                         f"where 0 means completely unjustified and 1 means completely justified.\n\n"
                         f"Text: {leave_text}\n\n"
                         f"Response format: Return only a decimal number between 0 and 1.")
                
                try:
                    # Try using the text-bison model which is available in older API versions
                    response = genai.generate_text(
                        model='models/text-bison-001',
                        prompt=prompt,
                        temperature=0.2,
                        max_output_tokens=10
                    )
                    
                    print("AI response:", response)
                    
                    # Extract probability from response
                    import re
                    if hasattr(response, 'text'):
                        text_response = response.text
                    elif hasattr(response, 'result'):
                        text_response = response.result
                    else:
                        text_response = str(response)
                    
                    number_match = re.search(r'(\d+\.\d+|\d+)', text_response)
                    
                    if number_match:
                        score = float(number_match.group(1))
                        # Ensure the score is between 0 and 1
                        if score > 1:
                            score = min(score / 100, 1.0) if score <= 100 else 1.0
                        return JsonResponse({"probability_score": score})
                    
                    # If regex fails, use the fallback
                    fallback_score = calculate_fallback_score(leave_text)
                    return JsonResponse({
                        "probability_score": fallback_score,
                        "note": "Could not extract a score from the AI response, using estimated score",
                        "raw_response": text_response
                    })
                    
                except Exception as api_error:
                    print(f"API error: {api_error}")
                    # Use fallback method
                    fallback_score = calculate_fallback_score(leave_text)
                    return JsonResponse({
                        "probability_score": fallback_score,
                        "note": "Using estimated score due to AI service limitation",
                        "error": str(api_error)
                    })
            
            except Exception as e:
                print(f"AI configuration error: {e}")
                # Use fallback scoring when AI is not available
                fallback_score = calculate_fallback_score(leave_text)
                return JsonResponse({
                    "probability_score": fallback_score,
                    "note": "Using estimated score"
                })
                
        except Exception as e:
            import traceback
            print(f"General error in get_probability_score: {str(e)}")
            print(traceback.format_exc())
            
            # Return a conservative default score
            return JsonResponse({
                "probability_score": 0.5,
                "note": "Using default score due to system error",
                "error": str(e)
            }, status=200)

    return JsonResponse({"error": "Invalid request method", "probability_score": 0.5}, status=200)

def schedules(request):
    return render(request, 'schedules.html')

@csrf_exempt
def test_gemini_api(request):
    """Test endpoint to verify Gemini API is working correctly"""
    if request.method == "GET":
        return render(request, 'test_gemini.html')
        
    try:
        # Check if API key is configured
        if not settings.GEMINI_API_KEY:
            return JsonResponse({
                "status": "error",
                "error": "API key is not configured in settings",
                "api_key_configured": False
            })
        
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # List available models
        models = []
        try:
            for model in genai.list_models():
                models.append(model.name)
        except Exception as model_error:
            models = ["Could not list models: " + str(model_error)]
            
        # Simple prompt that should return a basic response
        test_prompt = "Return a number between 0 and 1 as a test response. Just output the number."
        
        try:
            # Use models/text-bison-001 which is available in older API
            response = genai.generate_text(
                model='models/text-bison-001',
                prompt=test_prompt,
                temperature=0.1,
                max_output_tokens=10
            )
            
            # Format the response in a safe way
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'result'):
                response_text = response.result
            else:
                response_text = str(response)
                
            # Return success response with all information
            return JsonResponse({
                "status": "success",
                "api_key_configured": True,
                "api_key_preview": f"{settings.GEMINI_API_KEY[:4]}...{settings.GEMINI_API_KEY[-4:]}",
                "available_models": models,
                "raw_response": response_text,
                "response_type": str(type(response))
            })
        except Exception as api_error:
            # API error
            return JsonResponse({
                "status": "error",
                "error": f"API error: {str(api_error)}",
                "api_key_configured": True,
                "api_key_preview": f"{settings.GEMINI_API_KEY[:4]}...{settings.GEMINI_API_KEY[-4:]}",
                "available_models": models
            })
            
    except Exception as e:
        # General error
        import traceback
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "api_key_configured": bool(settings.GEMINI_API_KEY),
            "api_key_preview": f"{settings.GEMINI_API_KEY[:4]}...{settings.GEMINI_API_KEY[-4:]}" if settings.GEMINI_API_KEY else None
        })

# def job-details(request):
#     return render(request, 'contacts-list.html')
