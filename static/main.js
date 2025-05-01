function showDate(date = new Date()) {

    // Store weekday and month names so we can convert.
    const weekday_names = [
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ];
    const month_names = [
        "January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December"
    ];

    // Use some getters from w3schools.
    const day_name = weekday_names[date.getDay()];
    const month = month_names[date.getMonth()];
    const day_num = date.getDate();
    const year = date.getFullYear();

    // Format date to fit NYT
    const formatted_date = `${day_name} ${month} ${day_num}, ${year}`;

    // If there indeed is an element on the page, we will change its display.
    const element = document.getElementById('date');
    if (element) {
        element.innerHTML = `<span style='font-size: 15px;'>${formatted_date}<br><span style='font-size: 14px;'>Today's Paper`;
    }

    return formatted_date;
}

// Only run in browser when DOM is ready.
if (typeof window !== 'undefined' && typeof document !== 'undefined') {
    window.addEventListener('DOMContentLoaded', () => {
        showDate();
    });
}

module.exports = { showDate };
