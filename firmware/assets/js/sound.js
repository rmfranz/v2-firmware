$( "#sound" ).change(function() {
    $.post( "/sound", { volume: $(this).val()})
    .done(function( data ) {
        $("volume").text(data);
    });
});