document.addEventListener('DOMContentLoaded', function () {
    // Function to fetch events from the server
    function fetchEvents() {
        return fetch('/your-events')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data && data.events) {
                    // Process the received data and create the collapsible list
                    createCollapsibleList(data.events);
                } else {
                    console.error('Received data or events array is undefined.');
                }
            })
            .catch(error => console.error('Error fetching events:', error));
    }

    // Function to create the collapsible list
    function createCollapsibleList(events) {
        const collapse = document.getElementById('eventsCollapse');
        const eventsByMonth = groupEventsByMonth(events);

        // Iterate over months and create collapsible items
        for (const [month, monthEvents] of eventsByMonth) {
            const monthItem = document.createElement('div');
            monthItem.className = 'collapse-item';

            const monthHeader = document.createElement('h2');
            monthHeader.className = 'collapse-header';
            monthHeader.id = `month${month}`;
            monthHeader.innerHTML = `
                <button class="btn btn-primary" 
                type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#collapse${month}" 
                aria-expanded="false" 
                aria-controls="collapse${month}">
                    ${month}
                </button>
            `;

            const monthCollapse = document.createElement('div');
            monthCollapse.id = `collapse${month}`;
            monthCollapse.className = 'collapse';
            monthCollapse.setAttribute('aria-labelledby', `month${month}`);
            monthCollapse.setAttribute('data-bs-parent', '#eventsCollapse');

            const monthBody = document.createElement('div');
            monthBody.className = 'collapse-body';

            // Iterate over events in the month and create event items
            for (const event of monthEvents) {
                const eventItem = document.createElement('div');
                eventItem.innerHTML = `<p>${event.title}</p>
                                       <p>Date: ${event.date}</p>
                                       <p>Start Time: ${event.start_time}</p>
                                       <p>End Time: ${event.end_time}</p>`;
                monthBody.appendChild(eventItem);
            }

            monthCollapse.appendChild(monthBody);
            monthItem.appendChild(monthHeader);
            monthItem.appendChild(monthCollapse);
            collapse.appendChild(monthItem);
        }
    }

    // Function to group events by month
    function groupEventsByMonth(events) {
        const groupedEvents = new Map();
        for (const event of events) {
            const monthYear = event.date.substring(0, 7);  // Extract YYYY-MM from the date
            if (!groupedEvents.has(monthYear)) {
                groupedEvents.set(monthYear, []);
            }
            groupedEvents.get(monthYear).push(event);
        }
        return groupedEvents;
    }

    // Fetch events when the page is loaded
    fetchEvents();
});
