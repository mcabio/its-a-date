document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: function(info, successCallback, failureCallback) {
            // Fetch events from the server based on the current view
            // var user_id = getUserIDFromSession();  // Get user ID from the session or your preferred method
            console.log(info)
            const start = info.startStr;
            const end = info.endStr;
            const searchParams = new URLSearchParams({start, end})
            const url = '/publish-event?' + searchParams.toString()

            fetch(url, {
                method: 'GET',
                headers: {'Content-Type': 'application/json'},
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.events) {
                    // Process the received data and pass it to FullCalendar
                    var eventsData = data.events.map(event => ({
                        title: event.title,
                        description: event.description,
                        start: event.date + (event.start_time ? 'T' + event.start_time : ''),
                        end: event.date + (event.end_time ? 'T' + event.end_time : ''),
                        allDay: false
                    }));
            
                    successCallback(eventsData);  // Pass the events data to FullCalendar
                } else {
                    console.error('Received data or events array is undefined.');
                    failureCallback('Received data or events array is undefined.');  // Pass an error to FullCalendar
                }
            });
        },
        dateClick: function(info) {
            // Handle date clicks based on the view
            switch (info.view.type) {
                case 'dayGridMonth':
                    // Month view - Redirect to a page to add an event for the selected day
                    window.location.href = '/create-event?date=' + info.dateStr;
                    break;
                case 'timeGridWeek':
                    // Week view - Redirect to a page to add an event for the selected day
                    window.location.href = '/create-event?date=' + info.dateStr + '&time=' + info.date.getHours() + ':' + (info.date.getMinutes() < 30 ? '00' : '30');
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
});