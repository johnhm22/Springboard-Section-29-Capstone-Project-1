
$(".date").each(function(){
    let currDate = $(this).text();
    let newDate = moment(currDate).format("h:mm a, ddd Do MMMM");
    console.log(newDate);
    return $(this).text(newDate);
})

$(".koTime").each(function(){
    let currDate = $(this).text();
    let newDate = moment(currDate).format("h:mm a");
    console.log(newDate);
    return $(this).text(newDate);
})



