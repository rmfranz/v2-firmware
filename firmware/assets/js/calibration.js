$("#change_extruder").toggleClass( "k-modal-overlay--visible" );
var ip = "127.0.0.1";
var t0_activate =  true;
function get_offsets() {
    var t0_offset = 1;
    var t1_offset = 1;
    var t1_yoffset = 0;
    var t1_xoffset = 28;
    $.ajax({
        url: "/get-offsets",
        success: function (result) {
            t0_offset = result["t0_zoffset"];
            t1_offset = result["t1_zoffset"];
            t1_yoffset = result["t1_yoffset"];
            t1_xoffset = result["t1_xoffset"];
        },
        async: false
    });
    return {t0_offset, t1_offset, t1_yoffset, t1_xoffset}
}

var {t0_offset, t1_offset, t1_yoffset, t1_xoffset} = get_offsets();
$("#zoffset").text(t0_offset);
$("#yoffset").text(t1_yoffset);
$("#xoffset").text(t1_xoffset);

$("#plus_button").on("click", function() {
    $.ajax({url: "/z-offset-up", success: function(result){
        console.info(result)
    }});
    var oldValue = $("#zoffset").text();
    if (t0_activate) {
        t0_offset = Number((parseFloat(oldValue) + 0.025).toFixed(3));
        $("#zoffset").text(t0_offset);
    } else {
        t1_offset = Number((parseFloat(oldValue) + 0.025).toFixed(3));
        $("#zoffset").text(t1_offset);
    }
});

$("#minus_button").on("click", function() {
    $.ajax({url: "/z-offset-down", success: function(result){
        console.info(result)
    }});
    var oldValue = $("#zoffset").text();
    if (t0_activate) {
        t0_offset = Number((parseFloat(oldValue) - 0.025).toFixed(3));
        $("#zoffset").text(t0_offset);
    } else {
        t1_offset = Number((parseFloat(oldValue) - 0.025).toFixed(3));
        $("#zoffset").text(t1_offset);
    }
});

$("#t0_btn").on("click", function() {
    $('#change_extruder').toggleClass( "k-modal-overlay--visible" );
    $('#t0_btn').toggleClass( "k-grid-item--grey" );
    t0_activate = true;
    $.ajax({
        url: "/t0-calibration",
        success: function (result) {
            $("#zoffset").text(t0_offset);
            if(!$( "#t1_btn" ).hasClass("k-grid-item--grey")){
                $('#t1_btn').toggleClass( "k-grid-item--grey" );
            }
        }
    });
});

$("#t1_btn").on("click", function() {
    $('#change_extruder').toggleClass( "k-modal-overlay--visible" );
    $('#t1_btn').toggleClass( "k-grid-item--grey" );
    t0_activate = false;
    $.ajax({
        url: "/t1-calibration",
        success: function (result) {
            $("#zoffset").text(t1_offset);
            if(!$( "#t0_btn" ).hasClass("k-grid-item--grey")){
                $('#t0_btn').toggleClass( "k-grid-item--grey" );
            }
        }
    });
});

$("#save_zoffset").on("click", function() {
    $.post( "/z-offset-calibration", { zoffset_t0: t0_offset, zoffset_t1: t1_offset })
    .done(function( data ) {
        if(data == "ok"){
            $("#calibration_reset").toggleClass( "k-modal-overlay--visible" );
            window.location.href = "/back-calibration-selection";
        } else {
            //TODO: mostrar error
            $("#calibration_reset").toggleClass( "k-modal-overlay--visible" );
        }
    });
    $("#calibration_reset").toggleClass( "k-modal-overlay--visible" );
});

$("#25_points_calibration").on("click", function() {
    $("#grid_inspect").empty();
    $.ajax({url: "/points-25-calibration", success: function(result){
        console.info(result)
    }});
    $('#calibration_wait').toggleClass( "k-modal-overlay--visible" );
});

$("#inspect_grid_points").on("click", function() {
    $("#grid_inspect").empty();
    $.ajax({url: "/show-grid", success: function(result){
        console.info(result)
    }});
    $('#grid_modal').toggleClass( "k-modal-overlay--visible" );
});

$("#reset_grid").on("click", function() {
    $.ajax({url: "/reset-grid", success: function(result){
        console.info(result)
    }});
});

$("#x_plus_button").on("click", function() {
    var oldValue = $("#xoffset").text();
    t1_xoffset = Number((parseFloat(oldValue) + 0.05).toFixed(2));
    $("#xoffset").text(t1_xoffset);
});

$("#x_minus_button").on("click", function() {
    var oldValue = $("#xoffset").text();
    t1_xoffset = Number((parseFloat(oldValue) - 0.05).toFixed(2))
    $("#xoffset").text(t1_xoffset);
});

$("#y_plus_button").on("click", function() {
    var oldValue = $("#yoffset").text();
    t1_yoffset = Number((parseFloat(oldValue) + 0.05).toFixed(2));
    $("#yoffset").text(t1_yoffset);
});

$("#y_minus_button").on("click", function() {
    var oldValue = $("#yoffset").text();
    t1_yoffset = Number((parseFloat(oldValue) - 0.05).toFixed(2));
    $("#yoffset").text(t1_yoffset);
});

$("#save_xyoffset").on("click", function() {
    $.post( "/xy-offset-calibration", { yoffset: t1_yoffset, xoffset: t1_xoffset })
    .done(function( data ) {
        if(data == "ok"){
            $("#calibration_reset").toggleClass( "k-modal-overlay--visible" );
            window.location.href = "/back-calibration-selection";
        } else {
            //TODO: mostrar error!!
            $("#calibration_reset").toggleClass( "k-modal-overlay--visible" );
        }
    });
    $("#calibration_reset").toggleClass( "k-modal-overlay--visible" );
});


var ws_z_probe = new WebSocket("ws://" + ip + ":8888/z-probe");
ws_z_probe.onmessage = function (evt) {
    //$('#myModal').modal('hide');    
    $("#change_extruder").toggleClass( "k-modal-overlay--visible" );
};

var ws_25_points_calibration = new WebSocket("ws://" + ip + ":8888/probe-complete");
ws_25_points_calibration.onmessage = function (evt) {
    /*$('#myModal').modal('hide');
    $('#grid_modal').modal('show');*/
    $("#calibration_wait").toggleClass( "k-modal-overlay--visible" );
    $("#grid_modal").toggleClass( "k-modal-overlay--visible" );
};

var inspect_grid = new WebSocket("ws://" + ip + ":8888/inspect-grid");
inspect_grid.onmessage = function (evt) {
    var list = evt.data.split(" ")
    var append_td = "<tr>"
    for (var i = 0; i < list.length; i++) {
        append_td += "<td>" + list[i] + "</td>";
    }
    append_td += "</tr>"
    $( "#grid_inspect" ).append(append_td);    
};

$("#calibration_wait_close").on("click", function() {
    $("#calibration_wait").toggleClass( "k-modal-overlay--visible" );
});

$("#grid_modal_close").on("click", function() {
    $("#grid_modal").toggleClass( "k-modal-overlay--visible" );
});

$("#calibration_reset_close").on("click", function() {
    $("#calibration_reset").toggleClass( "k-modal-overlay--visible" );
});

$("#change_extruder_close").on("click", function() {
    $("#change_extruder").toggleClass( "k-modal-overlay--visible" );
});

$("#help_calibration").on("click", function() {
    $("#help_calibration_modal").toggleClass( "k-modal-overlay--visible" );
});

$("#help_calibration_modal_close").on("click", function() {
    $("#help_calibration_modal").toggleClass( "k-modal-overlay--visible" );
});