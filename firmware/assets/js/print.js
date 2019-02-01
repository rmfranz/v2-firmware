$('.file_selected').click(function () {
    $.post("/print", {file_path: $(this).data('path'), filename: $(this).data('filename')} )
    .done(function(data) {
       window.location.href = "/confirm-print";
    });
});

$("#print").click(function () {
    window.location.href = "/print";
});