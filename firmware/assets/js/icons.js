function get_cookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function set_connection_status(){
    $.get("/set_connection_status").done(function (data){
        if(data.cloud_status == "connected"){
            $("#cloud_icon").attr("src","/static/images/icon_nube-conectada.svg");
        }
        if(data.wifi_status == "wlan0"){
            $("#wifi_icon").attr("src","/static/images/icon_wifi-conectado.svg");
        }
    })
};

var wifi_status = get_cookie("wifi_status");
var cloud_status = get_cookie("cloud_status");

if(wifi_status == "" || cloud_status == ""){
    set_connection_status();
}

setInterval(set_connection_status, 30000);