

// document.addEventListener('DOMContentLoaded', function() {
//     var calendarEl = document.getElementById('calendar');
//     var selectedDate; // Variable to store the selected date

//     var calendar = new FullCalendar.Calendar(calendarEl, {
//         initialView: 'dayGridMonth',
//         headerToolbar: {
//             center: 'addEventButton'
//         },
//         customButtons: {
//             addEventButton: {
//                 text: 'add event...',
//                 click: function() {
//                     var dateStr = prompt('Enter a date in YYYY-MM-DD format');
//                     var date = new Date(dateStr + 'T00:00:00'); // will be in local time

//                     if (!isNaN(date.valueOf())) { // valid?
//                         selectedDate = date; // Set the selected date
//                         // Redirect to /create-event with the selected date
//                         window.location.href = '/create-event?date=' + dateStr;
//                     } else {
//                         alert('Invalid date.');
//                     }
//                 }
//             }
//         }
//     });

//     calendar.render();

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: function (fetchInfo, successCallback, failureCallback) {
            // Get user_id from the session (you need to set this on the server side when the user logs in)
            var user_id = getUserIDFromSession(); // Implement this function to get user_id from session

            // Make an AJAX request to fetch events from the server
            fetch('/your-events', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: user_id,
                    event_id: fetchInfo.event_id,  // You may update this part based on your logic
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Process the retrieved events
                successCallback(data.events);
            })
            .catch(error => {
                console.error('Error fetching events:', error);
                failureCallback(error);
            });
        },
        dateClick: function(info) {
            alert('clicked ' + info.dateStr);
        },
        select: function(info) {
            alert('selected ' + info.startStr + ' to ' + info.endStr);
        }        
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
                start: selectedDate.toISOString().slice(0, 10) + 'T' + startTime,
                end: selectedDate.toISOString().slice(0, 10) + 'T' + endTime,
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