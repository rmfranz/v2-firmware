var ws_error_handler = new WebSocket("ws://" + ip + ":8888/error-handler");
ws_error_handler.onmessage = function (evt) {
    $("#error_code").text(evt.data)
    $("#error_modal").toggleClass( "k-modal-overlay--visible" );
};

$("#error_modal_close").on("click", function() {
    $("#error_modal").toggleClass( "k-modal-overlay--visible" );
});