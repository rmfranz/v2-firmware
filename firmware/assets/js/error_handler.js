var ws_error_handler = new WebSocket("ws://" + ip + ":8888/error-handler");
ws_error_handler.onmessage = function (evt) {
    var error = evt.data
    if(typeof printing !== 'undefined' && printing && error == "ERR001"){
        $("#print_error_modal").toggleClass( "k-modal-overlay--visible" );
    } else if(error == "ERR001") {
        $("#communication_error_modal").toggleClass( "k-modal-overlay--visible" );
    } else {
        if(evt.data == "ERR002"){
            $("#error_code").text(evt.data)
        } else {
            $("#error_code").toggleClass("k-modal__warning");
            $("#error_text").text(evt.data)
        }
        $("#error_modal").toggleClass( "k-modal-overlay--visible" );
    }
};

$("#error_modal_close").on("click", function() {
    $("#error_modal").toggleClass( "k-modal-overlay--visible" );
});