var time_elapsed = 0;
function finish_load_filament() {
    $('#progress_bar').attr("value", 100);
    var div = '<div class="k-footer-right">'
        + '<a href="/back-load-unload" class="k-footer__btn k-footer__btn--yellow k-footer__btn--wide">'
        + word + '</a></div>';
    $(".k-footer").append(div);
    $("#filament_action").toggleClass("k-modal__warning--grey");
    //$("#filament_action").toggleClass("k-modal__warning");
    can_extrude = true;
}

function load_filament_wait() {
    ++time_elapsed;
    var perc = Math.round(((time_elapsed/66)*50) + 50);
    if(perc == 100){
        finish_load_filament()
    } else {
        $('#progress_bar').attr("value", perc);
        setTimeout(load_filament_wait, 1000);
    }
}

function finish_extrude_more() {
    $("#extrude_more_modal").toggleClass("k-modal-overlay--visible");
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

$('#filament_action').click(function () {
    if(can_extrude){
        $("#extrude_more_modal").toggleClass("k-modal-overlay--visible");
        $.get("/extrude-more");
        setTimeout(finish_extrude_more, 40000);
    }
});