

function getUserIDFromSession() {
    // Assuming you set the user ID in a global variable on the server side
    return window.user_id;  // Replace with your actual logic to get user_id
}

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
  
    var calendar = new FullCalendar.Calendar(calendarEl, {
      timeZone: 'UTC',
      initialView: 'listWeek',
  
      // customize the button names,
      // otherwise they'd all just say "list"
      views: {
        listDay: { buttonText: 'list day' },
        listWeek: { buttonText: 'list week' },
        listMonth: { buttonText: 'list month' }
      },
  
      headerToolbar: {
        left: 'title',
        center: '',
        right: 'listDay,listWeek,listMonth'
      },
      events: function (fetchInfo, successCallback, failureCallback) {
        // Get user_id from the session (you need to set this on the server side when the user logs in)
        var user_id = getUserIDFromSession();
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
    });
  
    calendar.render();
  });
