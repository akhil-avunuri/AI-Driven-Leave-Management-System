document.addEventListener('DOMContentLoaded', function() {
    console.log("FullCalendar initialization started");
    var calendarEl = document.getElementById('calendar');
    
    if (!calendarEl) {
        console.error("Could not find calendar element!");
        return;
    }
    
    console.log("Calendar element found");
    
    // Format datetime-local inputs properly (YYYY-MM-DDThh:mm)
    function formatDateForInput(date) {
        var year = date.getFullYear();
        var month = (date.getMonth() + 1).toString().padStart(2, '0');
        var day = date.getDate().toString().padStart(2, '0');
        var hours = date.getHours().toString().padStart(2, '0');
        var minutes = date.getMinutes().toString().padStart(2, '0');
        
        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek', // Default view: Week
        initialDate: new Date().toISOString().split("T")[0], // Set initial date dynamically
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        slotMinTime: '06:00:00', // Start time for day view
        slotMaxTime: '22:00:00', // End time for day view
        allDaySlot: false,      // Hide the all-day slot
        slotDuration: '00:30:00', // 30-minute slots
        slotLabelInterval: '01:00:00', // Show hour labels
        timeZone: 'local',      // Use local timezone
        eventTimeFormat: { hour: '2-digit', minute: '2-digit', hour12: false },

        // Prevent event overlap
        eventOverlap: false,

        // ✅ Fetch schedules from Django backend
        events: function(fetchInfo, successCallback, failureCallback) {
            var apiUrl = "/admin_role/api/get_schedules/";
            console.log("Fetching schedules from:", apiUrl);
            
            fetch(apiUrl)
                .then(response => {
                    console.log("Got response:", response.status, response.statusText);
                    if (!response.ok) {
                        throw new Error('Network error: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Schedules received:", data);
                    
                    // ✅ Format events properly with timezone handling
                    let formattedEvents = data.map(event => {
                        console.log("Processing event:", event);
                        // Parse the ISO strings directly - FullCalendar will handle timezone with timeZone: 'local'
                        return {
                            id: event.id,
                            title: event.title || event.section_name,
                            start: event.start,
                            end: event.end
                        };
                    });
                    
                    console.log("Formatted events:", formattedEvents);
                    successCallback(formattedEvents);
                })
                .catch(error => {
                    console.error("Error fetching schedules:", error);
                    failureCallback(error);
                });
        },

        eventDidMount: function(info) {
            console.log("Event rendered:", info.event.id, info.event.title, info.event.start, info.event.end);
            
            // Add different colors based on time of day
            const eventHour = new Date(info.event.start).getHours();
            if (eventHour >= 6 && eventHour < 12) {
                // Morning events (6AM-12PM)
                info.el.classList.add('morning');
            } else if (eventHour >= 12 && eventHour < 17) {
                // Afternoon events (12PM-5PM)
                info.el.classList.add('afternoon');
            } else {
                // Evening events (5PM onwards)
                info.el.classList.add('evening');
            }
        },

        eventContent: function(arg) {
            return {
                html: `<div class="fc-event-title">${arg.event.title}</div>
                       <div class="fc-event-time">${new Date(arg.event.start).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})} - 
                       ${new Date(arg.event.end).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</div>`
            };
        },
        
        // Add click event to handle edit/delete
        eventClick: function(info) {
            var eventId = info.event.id;
            var eventTitle = info.event.title;
            var eventStart = info.event.start;
            var eventEnd = info.event.end;
            
            console.log("Event clicked:", eventId, eventTitle, eventStart, eventEnd);
            
            // Format date for input fields, properly handling timezone
            var startDateTime = new Date(eventStart);
            var endDateTime = new Date(eventEnd);
            
            var startFormatted = formatDateForInput(startDateTime);
            var endFormatted = formatDateForInput(endDateTime);
            
            console.log("Formatted dates for modal:", startFormatted, endFormatted);
            
            // Show modal with event data for editing
            $("#edit-section-name").val(eventTitle);
            $("#edit-start-time").val(startFormatted);
            $("#edit-end-time").val(endFormatted);
            $("#current-event-id").val(eventId);
            
            $("#editScheduleModal").modal("show");
        }
    });

    calendar.render();

    // ✅ Open modal when "New Schedule" button is clicked
    $("#btn-new-schedule").on("click", function(e) {
        e.preventDefault();
        console.log("New Schedule button clicked");
        $("#newScheduleModal").modal("show");
    });

    // ✅ Clear all schedules button
    $("#btn-clear-schedules").on("click", function(e) {
        e.preventDefault();
        if (confirm("Are you sure you want to delete all schedules? This cannot be undone.")) {
            console.log("Clear all schedules confirmed");
            fetch("/admin_role/clear_schedules/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to clear schedules');
                }
                // Refresh calendar
                calendar.refetchEvents();
                alert("All schedules have been cleared successfully.");
            })
            .catch(error => {
                console.error("Error clearing schedules:", error);
                alert("Error clearing schedules: " + error.message);
            });
        }
    });

    // ✅ Save schedule when "Save Schedule" button is clicked
    $("#save-schedule").on("click", function() {
        var sectionName = $("#section-name").val(),
            startTime = $("#start-time").val(),
            endTime = $("#end-time").val();

        console.log("Save Schedule clicked");
        console.log("Section Name:", sectionName);
        console.log("Start Time (local):", startTime);
        console.log("End Time (local):", endTime);
        
        // For debugging timezone issues
        console.log("Current browser timezone:", Intl.DateTimeFormat().resolvedOptions().timeZone);
        var startDate = new Date(startTime);
        var endDate = new Date(endTime);
        console.log("Start as Date object:", startDate);
        console.log("End as Date object:", endDate);
        console.log("Start ISO string:", startDate.toISOString());
        console.log("End ISO string:", endDate.toISOString());

        if (sectionName && startTime && endTime) {
            console.log("All fields are filled, sending fetch request...");
            var createScheduleUrl = $("#btn-new-schedule").data("create-schedule-url");
            
            console.log("Using createScheduleUrl:", createScheduleUrl);
            
            fetch(createScheduleUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    section_name: sectionName,
                    start_time: startTime,
                    end_time: endTime
                })
            })
            .then(response => {
                console.log("Fetch response status:", response.status);
                console.log("Fetch response headers:", response.headers);
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error('Network response was not ok: ' + response.statusText + ' - ' + text);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Server response:", data);
                
                // ✅ Navigate to the event's date
                calendar.gotoDate(data.start);
                console.log("Navigated to event date:", data.start);

                // ✅ Refetch events to ensure the calendar is up-to-date
                calendar.refetchEvents();
                console.log("Refetched events from server");

                // ✅ Close modal and reset form
                $("#newScheduleModal").modal("hide");
                console.log("Modal should be hidden now");
                $("#new-schedule-form")[0].reset();
            })
            .catch(error => {
                console.error("Error saving schedule:", error);
                let errorMessage = "An error occurred while saving the schedule.";
                
                // Try to extract a more specific error message
                if (error.message && error.message.includes("overlaps")) {
                    errorMessage = "This schedule overlaps with existing schedules. Please choose a different time.";
                }
                
                alert(errorMessage);
            });
        } else {
            console.log("Validation failed: Some fields are empty");
            alert("Please fill in all fields.");
        }
    });
    
    // ✅ Update schedule when "Update Schedule" button is clicked
    $("#update-schedule").on("click", function() {
        var eventId = $("#current-event-id").val();
        var sectionName = $("#edit-section-name").val();
        var startTime = $("#edit-start-time").val();
        var endTime = $("#edit-end-time").val();
        
        if (sectionName && startTime && endTime) {
            fetch(`/admin_role/api/update_schedule/${eventId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    section_name: sectionName,
                    start_time: startTime,
                    end_time: endTime
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error('Failed to update schedule: ' + text);
                    });
                }
                return response.json();
            })
            .then(data => {
                // Update the event in the calendar
                var event = calendar.getEventById(eventId);
                if (event) {
                    event.setProp('title', data.section_name);
                    event.setStart(data.start);
                    event.setEnd(data.end);
                }
                
                // Close modal and refetch events
                $("#editScheduleModal").modal("hide");
                calendar.refetchEvents();
                alert("Schedule updated successfully");
            })
            .catch(error => {
                console.error("Error updating schedule:", error);
                let errorMessage = "An error occurred while updating the schedule.";
                
                // Try to extract a more specific error message
                if (error.message && error.message.includes("overlaps")) {
                    errorMessage = "This schedule overlaps with existing schedules. Please choose a different time.";
                }
                
                alert(errorMessage);
            });
        } else {
            alert("Please fill in all fields.");
        }
    });
    
    // ✅ Delete schedule when "Delete Schedule" button is clicked
    $("#delete-schedule").on("click", function() {
        var eventId = $("#current-event-id").val();
        
        if (confirm("Are you sure you want to delete this schedule?")) {
            fetch(`/admin_role/api/delete_schedule/${eventId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error('Failed to delete schedule: ' + text);
                    });
                }
                
                // Remove the event from the calendar
                var event = calendar.getEventById(eventId);
                if (event) {
                    event.remove();
                }
                
                // Close modal
                $("#editScheduleModal").modal("hide");
                alert("Schedule deleted successfully");
            })
            .catch(error => {
                console.error("Error deleting schedule:", error);
                alert("Error deleting schedule: " + error.message);
            });
        }
    });
});
