var ip = "127.0.0.1"

var ws_cloud = new WebSocket("ws://" + ip + ":8888/cloud");
ws_cloud.onmessage = function (evt) {
    var command = evt.data
    if(command == "gcodes") {
        $("#waitModal").toggleClass( "k-modal-overlay--visible" );
        $.post("/print", {file_path: "/home/pi/cloud/cloud.gcode", filename: "cloud.gcode"} )
    } else if (command == "download_done") {
        window.location.href = "/print";
    } else if (command == "pause") {
        $.get( "/pausa" );
        $('#pausa').toggle( false );
        $('#resume').toggle( true );
    } else if (command == "unpause") {
        $.get( "/resume" );
        $('#pausa').toggle( true );
        $('#resume').toggle( false );
    } else if (command == "cancel") {
        window.location.href = "/cancelar";
    } else if (command == "connected") {
        window.location.href = "/setup";
    }
};