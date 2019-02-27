
var plate_position = 235;

$('#plate-up').click(function () {
    if(plate_position > 35) {
        $.ajax({url: "/plate-up", success: function(result){
            plate_position =  plate_position - 35;
         }, async: false});
    }
});

$('#plate-down').click(function () {
    if(plate_position < 235) {
        $.ajax({url: "/plate-down", success: function(result){
            plate_position =  plate_position + 35;
        }, async: false});
    }
});

$('#plate-home').click(function () {
    $.ajax({url: "/plate-home", success: function(result){
        plate_position = 235;
    }, async: false});
});
