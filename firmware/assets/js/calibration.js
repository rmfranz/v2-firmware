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