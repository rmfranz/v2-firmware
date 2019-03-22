$('.nozzle_selected').click(function () {
    var nozzle_size = $(this).data('nozzle');
    var nozzle = $(this).data('nozzle-tipe');
    window.location.href = "/nozzle/" + nozzle + "?size=" + nozzle_size;
});

$('#nozzle_save').click(function () {
    var nozzle_size = $(this).data('nozzle');
    var nozzle = $(this).data('nozzle-tipe');
    $.post( "/set-nozzle", { size: nozzle_size, nozzle: nozzle })
    .done(function( data ) {
        window.location.href = "/nozzles"
    });
});