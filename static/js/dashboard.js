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
                slotMinTime: userDayStartTime,
                slotMaxTime: userDayEndTime,
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
                            var eventsData = data.events.map(event => ({
                                title: event.title,
                                description: event.description,
                                start: event.start_date + (event.start_time ? 'T' + event.start_time : ''),
                                end: event.end_date + (event.end_time ? 'T' + event.end_time : ''),
                                allDay: false,
                                extendedProps: {
                                    event_id: event.event_id,  // Your unique identifier for the event
                                    // ... other additional properties
                                }
                            }));

                            successCallback(eventsData);
                        } else {
                            console.error('Received data or events array is undefined.');
                            failureCallback('Received data or events array is undefined.');
                        }
                    });
                },
                dateClick: function(info) {
                    // Handle date clicks based on the view
                    switch (info.view.type) {
                        case 'dayGridMonth':
                            window.location.href = '/create-event?start_date=' + info.dateStr;
                            break;
                        case 'timeGridWeek':
                            const formattedWeek = info.dateStr.slice(0, 10);
                            window.location.href = '/create-event?' +
                                'start_date=' + formattedWeek +
                                '&time=' + info.date.getHours() + ':' + (info.date.getMinutes() < 30 ? '00' : '30');
                            break;
                        case 'timeGridDay':
                            const formattedDay = info.dateStr.slice(0, 10);
                            window.location.href = '/create-event?' +
                                'start_date=' + formattedDay +
                                '&time=' + info.date.getHours() + ':' + (info.date.getMinutes() < 30 ? '00' : '30');
                            break;
                        default:
                            // Handle other views as needed
                    }
                },
                eventClick: function(info) {
                    console.log('!!!Event clicked!!!:', info);
                    console.log('!!!Event Object!!!:', info.event);
                    const event_id = info.event.extendedProps.event_id;
                    switch (info.view.type) {
                        case 'dayGridMonth':
                            window.location.href = '/edit-event/' + event_id;
                            break;
                        case 'timeGridWeek':
                            window.location.href = '/edit-event/' + event_id;
                            break;
                        case 'timeGridDay':
                            window.location.href = '/edit-event/' + event_id;
                            break;
                        case 'listMonth':
                            window.location.href = '/edit-event/' + event_id;
                            break;
                    
                        default:
                            // Handle other views as needed
                    }
                },
            });

            calendar.render();
        } else {
            console.error('User preferences not available.');
        }
    })
    .catch(error => {
        console.error('Error fetching user preferences:', error);
    });
});
