$(".lang").click(function() {
    $.post( "/language", {language: $(this).data('lang')})
    .done(function( data ) {
        window.location.href = "/language";
    });
});