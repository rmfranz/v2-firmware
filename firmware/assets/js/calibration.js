var ip = "192.168.0.24"

$("#plus_button").on("click", function() {
    $.ajax({url: "/z-offset-up", success: function(result){
        console.info(result)
    }});
    var oldValue = $("#zoffset").val();
    var newVal = Number((parseFloat(oldValue) + 0.025).toFixed(3));
    $("#zoffset").val(newVal);
});

$("#minus_button").on("click", function() {
    $.ajax({url: "/z-offset-down", success: function(result){
        console.info(result)
    }});
    var oldValue = $("#zoffset").val();
    newVal = Number((parseFloat(oldValue) - 0.025).toFixed(3));
    $("#zoffset").val(newVal);
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