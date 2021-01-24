
$(".date").each(function(){
    let currDate = $(this).text();
    let newDate = moment(currDate).format("h:mm a, ddd Do MMMM");
    return $(this).text(newDate);
})

$(".koTime").each(function(){
    let currDate = $(this).text();
    let newDate = moment(currDate).format("h:mm a");
    return $(this).text(newDate);
})



