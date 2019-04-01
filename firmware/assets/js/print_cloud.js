
$.get("/get-cloud-queue").done(function (data) {
    var resp = data.resp
    var select = $("#cloud_files");
    for (var i = 0; i < resp.length; i++) {
        var d = '<div class="k-block-2 file_selected" data-job_id="' + resp[i].id + '" >'
        d += '<div class="k-block-2__left"><div class="k-block-2__img-container"> </div> <p>' + resp[i].filename + '</p> </div> </div>'
        select.append(d);
    }
    $("#waiting_info").toggleClass("initiallyHidden");
});

$('.file_selected').click(function () {
    $("#wait_fetching_modal").toggleClass("k-modal-overlay--visible");    
    window.location.href = "/confirm-cloud-print?job_id=" + $(this).data('job_id');
});