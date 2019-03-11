var ip = "127.0.0.1";
var paused = false;

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
    paused = true;
    $.get("/pausa");
    $('#pausa').toggle(false);
    $('#resume').toggle(true);
});

$('#resume').click(function () {
    paused = false;
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

$('#cancel_modal_no').click(function () {
    $("#cancel_modal").toggleClass("k-modal-overlay--visible");
});

$("#cancel_modal_yes").click(function () {
    $("#cancel_modal").toggleClass("k-modal-overlay--visible");
    $("#wait_cancel_modal").toggleClass("k-modal-overlay--visible");
    $.get("/cancelar");
    window.location.href = "/home";
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
    if(!paused){        
        ++totalSeconds;
        secondsLabel.innerHTML = pad(totalSeconds % 60);
        minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
        hoursLabel.innerHTML = pad(parseInt(totalSeconds / 3600));
    }
}

if (printing) {
    var line = 0;
    var totalLines = 0;
    $.ajax({
        url: "/print-total-lines",
        success: function (result) {
            totalLines = parseInt(result)
        },
        async: false
    });
    var ws_print_finished = new WebSocket("ws://" + ip + ":8888/print-finished");
    ws_print_finished.onmessage = function (evt) {
        if(!paused){
            var time = document.getElementById("hours").innerHTML + ":" + document.getElementById("minutes").innerHTML;
            $.post("/print-end", { time_printing: time})
                .done(function (data) {
                    window.location.href = "/print-end";
                });
        }
    };
    var ws_line_sended = new WebSocket("ws://" + ip + ":8888/line-sended");
    ws_line_sended.onmessage = function (evt) {
        ++line;
        if(totalLines != 0){
            $('#progress_bar').attr("value", parseInt((line * 100) / totalLines));
        } else {
            console.log("totalLines error")
        }
    };
    var minutesLabel = document.getElementById("minutes");
    var secondsLabel = document.getElementById("seconds");
    var hoursLabel = document.getElementById("hours");
    var totalSeconds = 0;
    setInterval(setTime, 1000);
}