from django.shortcuts import render, redirect, get_object_or_404
from employees.models import leaveapplication
from django.contrib import messages
from django.core.mail import send_mail
import google.generativeai as genai
from django.conf import settings
import re

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def categorize_leave(description):
    """Use AI to categorize the leave description into predefined categories"""
    try:
        # Make sure API key is configured
        if not settings.GEMINI_API_KEY:
            return "Uncategorized"

        # Create a prompt for categorizing leave
        prompt = (f"Analyze this leave request description and categorize it into EXACTLY ONE of these categories: "
                 f"'Urgent Medical', 'Health Related', 'Family Emergency', 'Vacation', 'Personal', or 'Other'. "
                 f"Return ONLY the category name as a single word or phrase, nothing else.\n\n"
                 f"Description: {description}")
        
        try:
            # Try using the text-bison model which is available in older API versions
            response = genai.generate_text(
                model='models/text-bison-001',
                prompt=prompt,
                temperature=0.1,
                max_output_tokens=10
            )
            
            # Extract category from response
            if hasattr(response, 'text'):
                text_response = response.text.strip()
            elif hasattr(response, 'result'):
                text_response = response.result.strip()
            else:
                text_response = str(response).strip()
            
            # Normalize the category (handle potential variations)
            text_response = text_response.replace('"', '').replace("'", "").strip()
            
            # Define valid categories
            valid_categories = ['Urgent Medical', 'Health Related', 'Family Emergency', 'Vacation', 'Personal', 'Other']
            
            # Match the response to closest valid category
            for category in valid_categories:
                if category.lower() in text_response.lower():
                    return category
            
            # Fallback based on keywords if exact match not found
            if any(kw in description.lower() for kw in ['sick', 'doctor', 'hospital', 'health', 'medical', 'ill']):
                return 'Health Related'
            elif any(kw in description.lower() for kw in ['urgent', 'emergency', 'immediate']):
                return 'Urgent Medical'
            elif any(kw in description.lower() for kw in ['family', 'relative', 'parent', 'child', 'spouse']):
                return 'Family Emergency'
            elif any(kw in description.lower() for kw in ['vacation', 'trip', 'holiday', 'travel']):
                return 'Vacation'
            else:
                return 'Personal'
                
        except Exception as api_error:
            print(f"API error in categorize_leave: {api_error}")
            # Fallback to keyword-based categorization
            if any(kw in description.lower() for kw in ['sick', 'doctor', 'hospital', 'health', 'medical', 'ill']):
                return 'Health Related'
            elif any(kw in description.lower() for kw in ['urgent', 'emergency', 'immediate']):
                return 'Urgent Medical'
            elif any(kw in description.lower() for kw in ['family', 'relative', 'parent', 'child', 'spouse']):
                return 'Family Emergency'
            elif any(kw in description.lower() for kw in ['vacation', 'trip', 'holiday', 'travel']):
                return 'Vacation'
            else:
                return 'Personal'
    
    except Exception as e:
        print(f"Error in categorize_leave: {e}")
        return "Uncategorized"

def leave_list(request):
    leave_applications = leaveapplication.objects.filter(status="Pending")
    
    # Add category for each leave application
    for leave in leave_applications:
        leave.category = categorize_leave(leave.leave_description)
        
    return render(request, 'leave_list.html', {'leave_applications': leave_applications})

def leave_description(request, leave_id):
    leave = get_object_or_404(leaveapplication, id=leave_id)
    # Add category for the leave
    leave.category = categorize_leave(leave.leave_description)
    return render(request, 'leave_description.html', {'leave': leave})

def update_leave_status(request, leave_id, status):
    leave = get_object_or_404(leaveapplication, id=leave_id)
    leave.status = status
    leave.save()

    if status == 'Approved':
        send_mail(
            'Leave Application Approved',
            f'Hello {leave.employee_name},\n\nYour leave application has been approved.\n\nBest regards,\nYour Company',
            'akhilavunoori@gmail.com',  # From email
            ['laddu29942@gmail.com'],  # To email (replace with the desired static email address)
            fail_silently=False,
        )

    messages.success(request, f'Leave application {status.lower()}.')
    return redirect('leave_list')