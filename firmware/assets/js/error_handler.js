var ws_error_handler = new WebSocket("ws://" + ip + ":8888/error-handler");
ws_error_handler.onmessage = function (evt) {
    var error = evt.data
    if(typeof printing !== 'undefined' && printing && error == "ERR001"){
        $("#print_error_modal").toggleClass( "k-modal-overlay--visible" );
    } else if(error == "ERR001") {
        $("#communication_error_modal").toggleClass( "k-modal-overlay--visible" );
    } else {
        $("#error_code").text(evt.data)
        $("#error_modal").toggleClass( "k-modal-overlay--visible" );
    }
};

$("#error_modal_close").on("click", function() {
    $("#error_modal").toggleClass( "k-modal-overlay--visible" );
});