

// document.addEventListener('DOMContentLoaded', function() {
//     var calendarEl = document.getElementById('calendar');
  
//     var calendar = new FullCalendar.Calendar(calendarEl, {
//       timeZone: 'UTC',
//       headerToolbar: {
//         left: 'prev,next today',
//         center: 'title',
//         right: 'dayGridMonth,timeGridWeek,timeGridDay'
//       },
//       editable: true,
//       dayMaxEvents: true // when too many events in a day, show the popover
//     //   events: '/api/demo-feeds/events.json?overload-day'
//     });
  
//     calendar.render();
//   });

// document.addEventListener('DOMContentLoaded', function() {
//     var calendarEl = document.getElementById('calendar');
  
//     var calendar = new FullCalendar.Calendar(calendarEl, {
//       initialView: 'dayGridMonth',
//       headerToolbar: {
//         center: 'addEventButton'
//       },
//       customButtons: {
//         addEventButton: {
//           text: 'add event...',
//           click: function() {
//             var dateStr = prompt('Enter a date in YYYY-MM-DD format');
//             var date = new Date(dateStr + 'T00:00:00'); // will be in local time
  
//             if (!isNaN(date.valueOf())) { // valid?
//               calendar.addEvent({
//                 title: 'dynamic event',
//                 start: date,
//                 allDay: true
//               });
//               alert('Great. Now, update your database...');
//             } else {
//               alert('Invalid date.');
//             }
//           }
//         }
//       }
//     });
  
//     calendar.render();
//   });

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            center: 'addEventButton'
        },
        customButtons: {
            addEventButton: {
                text: 'add event...',
                click: function() {
                    var dateStr = prompt('Enter a date in YYYY-MM-DD format');
                    var date = new Date(dateStr + 'T00:00:00'); // will be in local time

                    if (!isNaN(date.valueOf())) { // valid?
                        // Redirect to /create-event with the selected date
                        window.location.href = '/create-event?date=' + dateStr;
                    } else {
                        alert('Invalid date.');
                    }
                }
            }
        }
    });

    calendar.render();
});
