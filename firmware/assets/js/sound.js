$( "#sound" ).change(function() {
    $.post( "/sound", { volume: $(this).val()})
    .done(function( data ) {
        document.getElementById("audio").play();
        $("#volume").text(data);
    });
});