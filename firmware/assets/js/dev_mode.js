$("#enable_ssh").on("click", function () {
    $.get("/ssh-enable");
});

$("#disable_ssh").on("click", function () {
    $.get("/ssh-disable");
});

$("#enable_dev_mode").on("click", function () {
    $.get("/enable-dev-mode");
});

$("#disable_dev_mode").on("click", function () {
    $.get("/disable-dev-mode");
});

$("#reset_board").on("click", function () {
    $("#reset_board_modal").toggleClass("k-modal-overlay--visible");
});

$("#confirm_reset").on("click", function () {
    $("#reset_board_modal").toggleClass("k-modal-overlay--visible");
    $("#wait_reset_board_modal").toggleClass("k-modal-overlay--visible");
    $.get("/reset-board-uuid").done(function( data ) {
        if(data == "ok"){
            $("#reset_ok").toggleClass("initiallyHidden");
        } else if(data == "01"){
            $("#error_board").append("ERROR: Not board founded")
        } else if(data == "02") {
            $("#error_board").append("ERROR: Other usb founded")
        } else {
            $("#reset_ok").toggleClass("initiallyHidden");
        }
    });
});

$("#reset_ok_btn").on("click", function () {
    $("#wait_reset_board_modal").toggleClass("k-modal-overlay--visible");
});