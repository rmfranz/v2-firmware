$('#red').click(function () {
    $.ajax({url: "/lights/red", success: function(result){
        console.info(result)
    }});
});
$('#green').click(function () {
    $.ajax({url: "/lights/green", success: function(result){
        console.info(result)
    }});
});
$('#blue').click(function () {
    $.ajax({url: "/lights/blue", success: function(result){
        console.info(result)
    }});
});
$('#other').click(function () {
    $.ajax({url: "/lights/other", success: function(result){
        console.info(result)
    }});
});
$('#off').click(function () {
    $.ajax({url: "/lights/off", success: function(result){
        console.info(result)
    }});
});

$("#lights_switch").click(function () {
    if(lights_on) {
        $.ajax({url: "/lights/off", success: function(result){
            $("#lights").attr("src","/static/images/icon_luz-apagada.svg");
        }});
        lights_on = false;
    } else {
        $.ajax({url: "/lights/blue", success: function(result){
            $("#lights").attr("src","/static/images/icon_luz-prendida.svg");
        }});
        lights_on = true;
    }
});