$('.file_selected').click(function () {
    $.post("/print", { file_path: $(this).data('path'), filename: $(this).data('filename') })
    .done(function (data) {
        window.location.href = "/confirm-print";
    });
});

$("#print").click(function () {
    $("#waitModal").toggleClass("k-modal-overlay--visible");
    window.location.href = "/print";
});

/*  OLD
countDownDate = new Date();
// Update the count down every 1 second
var x = setInterval(function () {
    // Get todays date and time
    var now = new Date().getTime();
    // Find the distance between now an the count down date
    var distance = now - countDownDate.getTime();
    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    // Output the result in an element with id="demo"
    document.getElementById("timer").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
}, 1000);
*/

$('#pausa').click(function () {
    $.get("/pausa");
    $('#pausa').toggle(false);
    $('#resume').toggle(true);
});

$('#resume').click(function () {
    $.get("/resume");
    $('#pausa').toggle(true);
    $('#resume').toggle(false);
});

$('#cancel').click(function () {
    $("#cancel_modal").toggleClass("k-modal-overlay--visible");
});

$('#cancel_modal_close').click(function () {
    $("#cancel_modal").toggleClass("k-modal-overlay--visible");
});

function pad(val) {
    var valString = val + "";
    if (valString.length < 2) {
        return "0" + valString;
    } else {
        return valString;
    }
}

function setTime() {
    ++totalSeconds;
    secondsLabel.innerHTML = pad(totalSeconds % 60);
    minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
    hoursLabel.innerHTML = pad(parseInt(totalSeconds / 3600));
}

if(printing){
    var minutesLabel = document.getElementById("minutes");
    var secondsLabel = document.getElementById("seconds");
    var hoursLabel = document.getElementById("hours");
    var totalSeconds = 0;
    setInterval(setTime, 1000);
}