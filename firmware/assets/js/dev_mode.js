$("#enable_ssh").on("click", function () {
    $.get("/ssh-enable").done($("#ssh_enable_modal").toggleClass("k-modal-overlay--visible"));
});

$("#disable_ssh").on("click", function () {
    $.get("/ssh-disable").done($("#ssh_disable_modal").toggleClass("k-modal-overlay--visible"));
});

$("#enable_dev_mode").on("click", function () {
    $.get("/enable-dev-mode").done($("#done_modal").toggleClass("k-modal-overlay--visible"));
});

$("#disable_dev_mode").on("click", function () {
    $.get("/disable-dev-mode").done($("#done_modal").toggleClass("k-modal-overlay--visible"));
});

$("#enable_debug").on("click", function () {
    $.get("/toggle-debug?debug=enable").done($("#conf_reset_modal").toggleClass("k-modal-overlay--visible"));
});

$("#disable_debug").on("click", function () {
    $.get("/toggle-debug?debug=disable").done($("#conf_reset_modal").toggleClass("k-modal-overlay--visible"));
});

$("#get_log").on("click", function () {
    $("#wait_usb").toggleClass("k-modal-overlay--visible");
    $.get("/get-log").done(function( data ) {
        if(data == "ok"){
            $("#wait_usb").toggleClass("k-modal-overlay--visible");
            $("#done_modal").toggleClass("k-modal-overlay--visible");
        } else {
            $("#wait_usb").toggleClass("k-modal-overlay--visible");
            $("#error_usb_modal").toggleClass("k-modal-overlay--visible");
        }
    });
});

$("#reset_board").on("click", function () {
    $("#reset_board_modal").toggleClass("k-modal-overlay--visible");
});

$("#reset_mac").on("click", function () {
    $.get("/reset-mac").done($("#conf_reset_modal").toggleClass("k-modal-overlay--visible"));;
});

$("#restore_user_pref_btn").on("click", function() {
    $('#warning_reset_user_modal').toggleClass( "k-modal-overlay--visible" );
});

$("#restore_user_pref").on("click", function () {
    $.get("/restore-user-pref").done($("#conf_reset_modal").toggleClass("k-modal-overlay--visible"));;
    $('#warning_reset_user_modal').toggleClass( "k-modal-overlay--visible" );
});

$("#reset_user_pref_no").on("click", function() {
    $('#warning_reset_user_modal').toggleClass( "k-modal-overlay--visible" );
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

$("#done_modal_close").on("click", function () {
    $("#done_modal").toggleClass("k-modal-overlay--visible");
});
$("#ssh_enable_modal_close").on("click", function () {
    $("#ssh_enable_modal").toggleClass("k-modal-overlay--visible");
});
$("#ssh_disable_modal_close").on("click", function () {
    $("#ssh_disable_modal").toggleClass("k-modal-overlay--visible");
});

$("#conf_reset_modal_close").on("click", function () {
    $("#conf_reset_modal").toggleClass("k-modal-overlay--visible");
});

$("#error_usb_modal_close").on("click", function () {
    $("#error_usb_modal").toggleClass("k-modal-overlay--visible");
});