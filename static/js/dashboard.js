

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
    var selectedDate;
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        dateClick: function(info) {
            selectedDate = info.date; // Set selectedDate to the clicked date
            if (info.resource && info.resource.id) {
                alert('clicked ' + info.dateStr + ' on resource ' + info.resource.id);
            } else {
                alert('clicked ' + info.dateStr + ' on no resource');
            }
        },
        select: function(info) {
            if (info.resource && info.resource.id) {
                alert('selected ' + info.startStr + ' to ' + info.endStr + ' on resource ' + info.resource.id);
            } else {
                alert('selected ' + info.startStr + ' to ' + info.endStr + ' on no resource');
            }
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

            console.log('selectedDate:', selectedDate);
            console.log('startTime:', startTime);
            console.log('endTime:', endTime);

            // Add the event to the calendar
            calendar.addEvent(eventData);

            console.log(calendar.getEvents());

            // Optionally, you can clear the form or perform other actions

            // Reset the form
            form.reset();
        });
    }
});

