var time_elapsed = 0;
var word = "{{_("calibration_save")}}"
function finish_load_filament() {
    $('#progress_bar').attr("value", 100);
    var div = '<div class="k-footer-right">'
        + '<a href="/back-load-unload" class="k-footer__btn k-footer__btn--yellow k-footer__btn--wide">'
        + word + '</a></div>';
    $(".k-footer").append(div);
}

function load_filament_wait() {
    ++time_elapsed;
    var perc = Math.round((time_elapsed/66)*100);
    if(perc == 100){
        finish_load_filament()
    } else {
        $('#progress_bar').attr("value", perc);
        setTimeout(load_filament_wait, 1000);
    }
}

$('#cancel_load_unload_filament').click(function () {
    if(can_cancel){
        $("#cancel_modal").toggleClass("k-modal-overlay--visible");
    }
});

$('#cancel_modal_no').click(function () {
    $("#cancel_modal").toggleClass("k-modal-overlay--visible");
});

$("#cancel_modal_yes").click(function () {
    window.location.href = "/back-load-unload";
});