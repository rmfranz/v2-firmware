var ip = "127.0.0.1"

var t0 = 0;
var t1 = 0;
var bed = 0;
var amb = 0;
var is_heating = false;

function update_temperatures() {
   if(t0 == 0){
      $("#t0").text("27°C")
   } else {
      $("#t0").text(t0 + "°C")
   }
   if(t1 == 0){
      $("#t1").text("28°C")
   } else {
      $("#t1").text(t1 + "°C")
   }
   if(bed == 0){
      $("#plate").text("27°C")
   } else {
      $("#plate").text(bed + "°C")
   }
   if(amb == 0){
      $("#amb").text("28°C")
   } else {
      $("#amb").text(amb + "°C")
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
      unload_filament_wait();
   }
}

function heating_temp(temp, target) {
   if(filament_action == "filament_auto_load") {
      if(!fifty_reach){
         var perc = Math.round((temp/target)*50);
         if(perc == 50){
            fifty_reach = true;
         }
      }
   } else if(filament_action == "filament_auto_unload") {
      if(!eighty_reach){
         var perc = Math.round((temp/target)*80);
         if(perc == 80){
            eighty_reach = true;
         }
      }      
   }
   $('#progress_bar').attr("value", perc);
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
    if(typeof canceling !== 'undefined' && canceling){
       //$("#wait_cancel_modal").toggleClass("k-modal-overlay--visible");
       window.location.href = "/home";
     }
     if(is_heating && typeof printing !== 'undefined' && printing){
         is_heating = false;
         $.get("/lights/white");
      }
 };
 ws_bed.onmessage = function(evt) {
    var bed_data = evt.data
    var temp = bed_data.substring(bed_data.lastIndexOf(":") + 1, bed_data.lastIndexOf("/")).trim();
    $("#printing_action").text("Heating bed: " + temp);
    bed = temp;
    update_temperatures();
    if(!is_heating){
      is_heating = true;
      $.get("/lights/orange");
    }
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
    if(!is_heating){
      is_heating = true;
      $.get("/lights/orange");
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

 /*function set_board_uuid() {
   $.get("/set-board-uuid");
 }

 set_board_uuid();*/

 if(typeof in_extruder_control !== 'undefined'){

   function change_t0_buttons() {
      $("#t0_extrude").toggleClass("k-grid-item--grey");
      $("#t0_retract").toggleClass("k-grid-item--grey");
   }

   function change_t1_buttons() {
      $("#t1_extrude").toggleClass("k-grid-item--grey");
      $("#t1_retract").toggleClass("k-grid-item--grey");
   }

   function finish_extrude() {
      $("#extrude_modal").toggleClass("k-modal-overlay--visible");
   }
   
   function finish_retract() {
      $("#retract_modal").toggleClass("k-modal-overlay--visible");
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
         $("#extrude_modal").toggleClass("k-modal-overlay--visible");
         $.get("/ext_1/extrude");
         setTimeout(finish_extrude, 15000);
      }
   });
   $("#t0_retract").click(function () {
      if(t0_temp != 0 && t0 >= (t0_temp - (t0_temp * 0.05))){
         $("#retract_modal").toggleClass("k-modal-overlay--visible");
         $.get("/ext_1/retract");
         setTimeout(finish_retract, 3000);
      }
   });
   $("#t1_extrude").click(function () {
      if(t1_temp != 0 && t1 >= (t1_temp - (t1_temp * 0.05))){
         $("#extrude_modal").toggleClass("k-modal-overlay--visible");
         $.get("/ext_2/extrude");
         setTimeout(finish_extrude, 15000);
      }
   });
   $("#t1_retract").click(function () {
      if(t1_temp != 0 && t1 >= (t1_temp - (t1_temp * 0.05))){
         $("#retract_modal").toggleClass("k-modal-overlay--visible");
         $.get("/ext_2/retract");
         setTimeout(finish_retract, 3000);
      }
   });

   btn_changer();   
 }