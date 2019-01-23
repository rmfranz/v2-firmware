var ip = "192.168.0.24";
var t0_activate =  true;
function get_t0_t1_offset() {
    var t0_offset = 1;
    var t1_offset = 1;
    $.ajax({
        url: "/get-offsets",
        success: function (result) {
            t0_offset = result["t0_zoffset"];
            t1_offset = result["t1_zoffset"];
        },
        async: false
    });
    return {t0_offset, t1_offset}
}

var {t0_offset, t1_offset} = get_t0_t1_offset();
$("#zoffset").val(t0_offset);

$("#plus_button").on("click", function() {
    $.ajax({url: "/z-offset-up", success: function(result){
        console.info(result)
    }});
    var oldValue = $("#zoffset").val();
    if (t0_activate) {
        t0_offset = Number((parseFloat(oldValue) + 0.025).toFixed(3));
        $("#zoffset").val(t0_offset);
    } else {
        t1_offset = Number((parseFloat(oldValue) + 0.025).toFixed(3));
        $("#zoffset").val(t1_offset);
    }
});

$("#minus_button").on("click", function() {
    $.ajax({url: "/z-offset-down", success: function(result){
        console.info(result)
    }});
    var oldValue = $("#zoffset").val();
    if (t0_activate) {
        t0_offset = Number((parseFloat(oldValue) - 0.025).toFixed(3));
        $("#zoffset").val(t0_offset);
    } else {
        t1_offset = Number((parseFloat(oldValue) - 0.025).toFixed(3));
        $("#zoffset").val(t1_offset);
    }
});

$("#t0_btn").on("click", function() {
    $('#myModal').modal('show')
    t0_activate = true;
    $.ajax({
        url: "/t0-calibration",
        success: function (result) {
            $("#zoffset").val(t0_offset);
        }
    });
});

$("#t1_btn").on("click", function() {
    $('#myModal').modal('show')
    t0_activate = false;
    $.ajax({
        url: "/t1-calibration",
        success: function (result) {
            $("#zoffset").val(t1_offset);
        }
    });
});

$("#save_zoffset").on("click", function() {
    $.post( "/z-offset-calibration", { zoffset_t0: t0_offset, zoffset_t1: t1_offset })
    .done(function( data ) {
        if(data == "ok"){
            $('#myModal').modal('hide');
            window.location.href = "/back-calibration-selection";
        } else {
            $('#myModal').modal('hide');
        }
    });
    $('#myModal').modal('show')
});

$("#25_points_calibration").on("click", function() {
    $.ajax({url: "/points-25-calibration", success: function(result){
        console.info(result)
    }});
    $('#myModal').modal('show')
});

var ws_25_points_calibration = new WebSocket("ws://" + ip + ":8888/probe-complete");
ws_25_points_calibration.onmessage = function (evt) {
    $('#myModal').modal('hide')
};

var ws_z_probe = new WebSocket("ws://" + ip + ":8888/z-probe");
ws_z_probe.onmessage = function (evt) {
    $('#myModal').modal('hide')
};