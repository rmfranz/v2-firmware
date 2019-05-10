var ip = "127.0.0.1"

var ws_cloud = new WebSocket("ws://" + ip + ":8888/cloud");
ws_cloud.onmessage = function (evt) {
    var command = evt.data
    if(command == "gcodes") {
        $("#waitModal").toggleClass( "k-modal-overlay--visible" );
       // $.post("/print", {file_path: "/home/pi/cloud/cloud.gcode", filename: "cloud.gcode"} )
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
        $("#wait_cancel_modal").toggleClass("k-modal-overlay--visible");
        canceling = true;
        $.get("/cancel-cloud");
    } else if (command == "finish") {
        window.location.href = "/home";
    } else if (command == "connected") {
        $("#cloud_icon").attr("src","/static/images/icon_nube-conectada.svg");
        $.get("http://" + ip + ":9000/init-websockets");
        $.post( "/set-user-cloud-pref", { status: "connected"})
        .done(function( data ) {
            window.location.href = "/to-cloud";
        });        
    }
};