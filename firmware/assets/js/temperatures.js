var ip = "127.0.0.1"

var t0 = 0
var t1 = 0
var bed = 0
var amb = 0

function update_temperatures() {
   if(t0 == 0){
      $("#t0").text("")
   } else {
      $("#t0").text(t0)
   }
   if(t1 == 0){
      $("#t1").text("")
   } else {
      $("#t1").text(t1)
   }
   if(bed == 0){
      $("#plate").text("")
   } else {
      $("#plate").text(bed)
   }
   if(amb == 0){
      $("#amb").text("")
   } else {
      $("#amb").text(amb)
   }
}

function set_temperatures(data) {
    var temps = data.split("@")
    t0 = temps[0].substring(temps[0].indexOf(":") + 1, temps[0].indexOf("/")).trim()
    t1 = temps[1].substring(temps[1].indexOf(":") + 1, temps[1].indexOf("/")).trim()
    bed = temps[2].substring(temps[2].indexOf(":") + 1, temps[2].indexOf("/")).trim()
    amb = temps[3].substring(temps[3].indexOf(":") + 1, temps[3].indexOf("/")).trim()
    update_temperatures();
    /*$("#t0").text(t0)
    $("#t1").text(t1)
    $("#plate").text(bed)
    $("#amb").text(amb)*/
 }
 var ws_temps = new WebSocket("ws://" + ip + ":8888/temperatures");
 var ws_bed = new WebSocket("ws://" + ip + ":8888/heating-bed");
 var ws_nozzle = new WebSocket("ws://" + ip + ":8888/heating-nozzle");
 ws_temps.onmessage = function (evt) {
    set_temperatures(evt.data);
 };
 ws_bed.onmessage = function(evt) {
    var bed_data = evt.data
    var temp = bed_data.substring(bed_data.lastIndexOf(":") + 1, bed_data.lastIndexOf("/")).trim();
    $("#printing_action").text("Heating bed: " + temp);
    bed = temp;
    update_temperatures();
 };
 ws_nozzle.onmessage = function(evt) {
    var nozzle = evt.data
    var temp = nozzle.substring(nozzle.lastIndexOf(":") + 1, nozzle.lastIndexOf("/")).trim();
    var nozzle_type = nozzle.substring(nozzle.lastIndexOf("T") + 1, nozzle.lastIndexOf(":")).trim();
    if(nozzle_type == 0) {
      t0 = temp;
    } else if(nozzle_type == 1) {
      t1 = temp;
    }
    $("#printing_action").text("Heating nozzle: " + temp)
 };
 
 var call_temperatures_api = function () {
    $.ajax({url: "/get-temperatures", success: function(result){
       console.info(result)
    }});
    setTimeout(call_temperatures_api, 2000);
 };
 call_temperatures_api();

 function set_board_uuid() {
   $.get("/set-board-uuid");
 }

 set_board_uuid();