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