
$.get("/get-cloud-queue").done(function (data) {
    var resp = data.resp
    var select = $("#cloud_files");
    for (var i = 0; i < resp.length; i++) {
        var d = '<div class="k-block-2 file_selected" data-job_id="' + resp[i].id + '" data-filename="' + resp[i].filename + '">'
        d += '<div class="k-block-2__left"><div class="k-block-2__img-container"> </div> <p>' + resp[i].filename + '</p> </div> </div>'
        select.append(d);
    }
}
);