var motors = true;
$("#motors_switch").click(function () {
    if(motors) {
        $.ajax({url: "/turn-off-motors", success: function(result){
            $("#motors").attr("src","/static/images/icon_apagar-motores.svg");
        }});
        motors = false;
    } else {
        $.ajax({url: "/turn-on-motors", success: function(result){
            $("#motors").attr("src","/static/images/icon_apagar-motores.svg");
        }});
        motors = true;
    }
});