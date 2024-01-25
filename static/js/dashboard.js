document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    // Fetch user preferences from the server
    fetch('/user-preferences', {
        method: 'GET',
        credentials: 'include',  // Include credentials (cookies) in the request
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(userData => {
        if (userData && userData.user_preferences) {
            const userDayStartTime = userData.user_preferences.day_start_time;
            const userDayEndTime = userData.user_preferences.day_end_time;

            var calendar = new FullCalendar.Calendar(calendarEl, {
                themeSystem: 'bootstrap5',
                initialView: 'dayGridMonth',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
                },
                slotMinTime: userDayStartTime, // Set the minimum time based on user preferences
                slotMaxTime: userDayEndTime,   // Set the maximum time based on user preferences
                eventColor: '#613389',
                eventTextColor: '#E6D8EC',
                events: function(info, successCallback, failureCallback) {
                    // Fetch events from the server based on the current view
                    console.log(info);
                    const start = info.startStr;
                    const end = info.endStr;
                    const searchParams = new URLSearchParams({ start, end });
                    const url = '/api/event?' + searchParams.toString();

                    fetch(url, {
                        method: 'GET',
                        headers: { 'Content-Type': 'application/json' },
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data && data.events) {
                            // Process the received data and pass it to FullCalendar
                            var eventsData = data.events.map(event => ({
                                title: event.title,
                                description: event.description,
                                start: event.start_date + (event.start_time ? 'T' + event.start_time : ''),
                                end: event.end_date + (event.end_time ? 'T' + event.end_time : ''),
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
                            window.location.href = '/create-event?start_date=' + info.dateStr;
                            break;
                        case 'timeGridWeek':
                            // Week/Day view - Redirect to a page to add an event for the selected day and time
                            const formattedWeek = info.dateStr.slice(0, 10);  // Extract YYYY-MM-DD
                            const hours = info.date.getHours() < 10 ? '0' + info.date.getHours() : info.date.getHours();
                            const minutes = info.date.getMinutes() < 30 ? '00' : '30';
                            window.location.href = '/create-event?' +
                                'start_date=' + formattedWeek +
                                '&time=' + hours + ':' + minutes;
                            break;
                        case 'timeGridDay':
                            // Week/Day view - Redirect to a page to add an event for the selected day and time
                            const formattedDay = info.dateStr.slice(0, 10);  // Extract YYYY-MM-DD
                            window.location.href = '/create-event?' +
                                'start_date=' + formattedDay +
                                '&time=' + hours + ':' + minutes;
                            break;
                        default:
                            // Handle other views as needed
                    }
                },
            });

            calendar.render();
        } else {
            console.error('User preferences not available.');
            // Handle the case when user preferences are not available
        }
    })
    .catch(error => {
        console.error('Error fetching user preferences:', error);
        // Handle the error scenario
    });
});




