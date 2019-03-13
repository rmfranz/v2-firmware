$( "#sound" ).change(function() {
    $.post( "/sound", { volume: $(this).val()})
    .done(function( data ) {
        var audio = document.getElementById("audio");
        audio.pause();
        audio.currentTime = 0;
        audio.play();
        $("#volume").text(data);
    });
});