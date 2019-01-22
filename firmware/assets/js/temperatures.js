var ip = "192.168.0.24"

function set_temperatures(data) {
    var temps = data.split("@")
    var t0 = temps[0].substring(temps[0].indexOf(":") + 1, temps[0].indexOf("/")).trim()
    var t1 = temps[1].substring(temps[1].indexOf(":") + 1, temps[1].indexOf("/")).trim()
    var bed = temps[2].substring(temps[2].indexOf(":") + 1, temps[2].indexOf("/")).trim()
    var amb = temps[3].substring(temps[3].indexOf(":") + 1, temps[3].indexOf("/")).trim()
    $("#t0").text(t0)
    $("#t1").text(t1)
    $("#plate").text(bed)
    $("#amb").text(amb)
 }
 var ws_temps = new WebSocket("ws://" + ip + ":8888/temperatures");
 var ws_bed = new WebSocket("ws://" + ip + ":8888/heating-bed");
 var ws_nozzle = new WebSocket("ws://" + ip + ":8888/heating-nozzle");
 ws_temps.onmessage = function (evt) {
    set_temperatures(evt.data);
 };
 ws_bed.onmessage = function(evt) {
    var bed = evt.data
    var temp = bed.substring(bed.lastIndexOf(":") + 1, bed.lastIndexOf("/")).trim();
    $("#printing_action").text("Heating bed: " + temp)
 };
 ws_nozzle.onmessage = function(evt) {
    var nozzle = evt.data
    var temp = nozzle.substring(nozzle.lastIndexOf(":") + 1, nozzle.lastIndexOf("/")).trim();
    $("#printing_action").text("Heating nozzle: " + temp)
 };
 
 var call_temperatures_api = function () {
    $.ajax({url: "/get-temperatures", success: function(result){
       console.info(result)
    }});
    setTimeout(call_temperatures_api, 5000);
 };
 call_temperatures_api();