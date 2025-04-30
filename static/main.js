function showDate() {
    
    const date = new Date();

    // Store weekday and month names so we can convert
    const weekday_names = [
        "Sunday", "Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday"
    ];
    const month_names = [
        "January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December"
    ];

    // Use some getters from w3schools
    const day_name = weekday_names[date.getDay()];
    const month = month_names[date.getMonth()];
    const day_num = date.getDate();
    const year = date.getFullYear();

    // format date to fit NYT
    const formatted_date = `${day_name} ${month} ${day_num}, ${year}`;
    
    document.getElementById('date').innerHTML = "<span style='font-size: 15px;'>" + formatted_date + "<br><span style='font-size: 14px;'>Today's Paper";
}

showDate();
