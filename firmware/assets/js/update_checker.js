$.get("/check-update").done(function (data) {
    if (!data.result) {
        $('#updateModal').toggleClass("k-modal-overlay--visible");
        $.get("/update-board-config").done(function (data) {
            if (data.error == 1) {
                $('#board_not_found').toggleClass("initiallyHidden");
                $('#updateModal').toggleClass("k-modal-overlay--visible");
                $('#errorPutConfigModal').toggleClass("k-modal-overlay--visible");
            } else if (data.error == 2) {
                $('#put_config_error').toggleClass("initiallyHidden");
                $('#updateModal').toggleClass("k-modal-overlay--visible");
                $('#errorPutConfigModal').toggleClass("k-modal-overlay--visible");
            }
        })
    }
});

$("#update_modal_close").on("click", function () {
    $('#updateModal').toggleClass("k-modal-overlay--visible");
});