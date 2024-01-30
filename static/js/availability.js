document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('available-cal');

    // Fetch user preferences from the server
    fetch('/user-preferences', {
        method: 'GET',
        credentials: 'include',
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
                initialView: 'listMonth',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title'
                },
                slotMinTime: userDayStartTime,
                slotMaxTime: userDayEndTime,
                events: function(info, successCallback, failureCallback) {
                    // Fetch events from the server based on the current view
                    console.log('THIS IS INFO:', info);
                    const start = info.startStr;
                    const end = info.endStr;
                    const searchParams = new URLSearchParams({ start, end });
                    const url = '/api/availability?' + searchParams.toString();  // Updated URL
                    console.log('THIS IS THE URL:', url);
                    fetch(url, {
                        method: 'GET',
                        headers: { 'Content-Type': 'application/json' },
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data && data.availability) {
                            // Process the received data and pass it to FullCalendar
                            var availabilityData = data.availability.map(date => ({
                                title: ' ',
                                start: date,
                                allDay: true
                            }));

                            successCallback(availabilityData);
                        } else {
                            console.error('Received data or availability array is undefined.');
                            failureCallback('Received data or availability array is undefined.');
                        }
                    });
                },
                eventClick: function(info) {
                    console.log('Event clicked:', info);
                    // Handle date clicks based on the view
                    switch (info.view.type) {
                        case 'listMonth':
                            // Format the date to "yyyy-MM-dd" before appending it to the URL
                            const formattedDate = info.event.start.toISOString().split('T')[0];
                            window.location.href = '/create-event?start_date=' + formattedDate;
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
