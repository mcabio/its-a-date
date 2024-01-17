document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Your FullCalendar configuration options...
        dateClick: function(info) {
            // Handle date clicks based on the view
            switch (info.view.type) {
                case 'dayGridMonth':
                    // Month view - Redirect to a page to add an event for the selected day
                    window.location.href = '/create-event?date=' + info.dateStr;
                    break;
                case 'timeGridWeek':
                    // Week view - Redirect to a page to add an event for the selected day
                    window.location.href = '/create-event?date=' + info.dateStr;
                    break;
                case 'timeGridDay':
                    // Day view - Redirect to a page to add an event for the selected half-hour slot
                    window.location.href = '/create-event?date=' + info.dateStr + '&time=' + info.date.getHours() + ':' + (info.date.getMinutes() < 30 ? '00' : '30');
                    break;
                default:
                    // Handle other views as needed
            }
        },
    });

    calendar.render();

    // Handle form submission
    var form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting traditionally

            // Collect form data
            var formData = new FormData(form);
            var title = formData.get('title');
            var description = formData.get('description');
            var startTime = formData.get('start_time');
            var endTime = formData.get('end_time');

            // Construct FullCalendar event data
            var eventData = {
                title: title,
                description: description,
                start: info.date,
                end: info.date,
                allDay: false
            };

            // Add the event to the calendar
            calendar.addEvent(eventData);

            // Optionally, you can clear the form or perform other actions

            // Reset the form
            form.reset();
        });
    }
});

function getUserIDFromSession() {
    // Assuming you set the user ID in a global variable on the server side
    return window.user_id;  // Replace with your actual logic to get user_id
}
