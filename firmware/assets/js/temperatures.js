var ip = "127.0.0.1"

var t0 = 0
var t1 = 0
var bed = 0
var amb = 0

function update_temperatures() {
   if(t0 == 0){
      $("#t0").text("27")
   } else {
      $("#t0").text(t0)
   }
   if(t1 == 0){
      $("#t1").text("28")
   } else {
      $("#t1").text(t1)
   }
   if(bed == 0){
      $("#plate").text("27")
   } else {
      $("#plate").text(bed)
   }
   if(amb == 0){
      $("#amb").text("28")
   } else {
      $("#amb").text(amb)
   }
}

function extrude_retract(){
   if(filament_action == "filament_auto_load"){
      $.get("/extrude");
      can_cancel = false;
      $("#btn_filament_cancel").toggleClass("k-footer__btn--red");
      $("#btn_filament_cancel").toggleClass("k-footer__btn--grey");
      load_filament_wait();
   } else if(filament_action == "filament_auto_unload") {
      $.get("/retract")
      can_cancel = false;
      $("#btn_filament_cancel").toggleClass("k-footer__btn--red");
      $("#btn_filament_cancel").toggleClass("k-footer__btn--grey");
      finish_load_filament();
   }
}

function heating_temp(temp, target) {
   var perc = Math.round((temp/target)*100);
   $('#progress_bar_temp').attr("value", perc);
}

function set_temperatures(data) {
    var temps = data.split("@")
    t0 = temps[0].substring(temps[0].indexOf(":") + 1, temps[0].indexOf("/")).trim()
    t1 = temps[1].substring(temps[1].indexOf(":") + 1, temps[1].indexOf("/")).trim()
    bed = temps[2].substring(temps[2].indexOf(":") + 1, temps[2].indexOf("/")).trim()
    amb = temps[3].substring(temps[3].indexOf(":") + 1, temps[3].indexOf("/")).trim()
    update_temperatures();
    if(typeof in_filament !== 'undefined') {
       if(extruder == "ext_1") {
         var target = temps[0].substring(temps[0].indexOf("/") + 1).trim()
         heating_temp(parseFloat(t0), parseFloat(target));
         if(parseFloat(t0) >= parseFloat(target) && !first_reach) {
            temp_reach = true;
            first_reach = true;            
            extrude_retract();
         }
         if((parseFloat(t0) < (parseFloat(target) - 2)) && temp_reach) {
            $.post( "/maintain-temp", {target: target})
         }
       } else if(extruder == "ext_2") {
         var target = temps[1].substring(temps[1].indexOf("/") + 1).trim()
         heating_temp(parseFloat(t1), parseFloat(target));
         if(parseFloat(t1) >= parseFloat(target) && !first_reach) {
            temp_reach = true;
            first_reach = true;
            extrude_retract();
         }
         if((parseFloat(t1) < (parseFloat(target) - 2)) && temp_reach) {
            $.post( "/maintain-temp", {target: target})
         }
       }
    }
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
      update_temperatures();
    } else if(nozzle_type == 1) {
      t1 = temp;
      update_temperatures();
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

 if(typeof in_extruder_control !== 'undefined'){

   function change_t0_buttons() {
      $("#t0_extrude").toggleClass("k-grid-item--grey");
      $("#t0_retract").toggleClass("k-grid-item--grey");
   }

   function change_t1_buttons() {
      $("#t1_extrude").toggleClass("k-grid-item--grey");
      $("#t1_retract").toggleClass("k-grid-item--grey");
   }

   function btn_changer() {
      if(t0_temp != 0 && t0 >= (t0_temp - (t0_temp * 0.05))){
         if($("#t0_extrude").hasClass("k-grid-item--grey") &&
            $("#t0_retract").hasClass("k-grid-item--grey")){
            change_t0_buttons()
         }
      } else {
         if(!$("#t0_extrude").hasClass("k-grid-item--grey") &&
            !$("#t0_retract").hasClass("k-grid-item--grey")){
            change_t0_buttons()
         }
      }
      
      if (t1_temp != 0 && t1 >= (t1_temp - (t1_temp * 0.05))) {
         if($("#t1_extrude").hasClass("k-grid-item--grey") &&
            $("#t1_retract").hasClass("k-grid-item--grey")){
            change_t1_buttons()
         }
      } else {
         if(!$("#t1_extrude").hasClass("k-grid-item--grey") &&
            !$("#t1_retract").hasClass("k-grid-item--grey")){
            change_t1_buttons()
         }
      }

      setTimeout(btn_changer, 2000);
   }

   var t0_temp = 0;
   var t1_temp = 0;

   $.ajax({url: "/get-extruder-options", 
      success: function(result){
         t0_temp = parseInt(result["t0_temp"])
         t1_temp = parseInt(result["t1_temp"])
      },
      async: false
   });
   $("#t0_extrude").click(function () {
      if(t0_temp != 0 && t0 >= (t0_temp - (t0_temp * 0.05))){
         $.get("/ext_1/extrude");
      }
   });
   $("#t0_retract").click(function () {
      if(t0_temp != 0 && t0 >= (t0_temp - (t0_temp * 0.05))){
         $.get("/ext_1/retract");
      }
   });
   $("#t1_extrude").click(function () {
      if(t1_temp != 0 && t1 >= (t1_temp - (t1_temp * 0.05))){
         $.get("/ext_2/extrude");
      }
   });
   $("#t1_retract").click(function () {
      if(t1_temp != 0 && t1 >= (t1_temp - (t1_temp * 0.05))){
         $.get("/ext_2/retract");
      }
   });

   btn_changer();   
 }