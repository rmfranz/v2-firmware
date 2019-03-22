$('.nozzle_selected').click(function () {
    var nozzle_size = $(this).data('nozzle');
    var nozzle = $(this).data('nozzle-tipe');
    window.location.href = "/nozzle/" + nozzle + "?size=" + nozzle_size;
});