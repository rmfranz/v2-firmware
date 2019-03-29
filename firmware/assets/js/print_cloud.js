
$.get("/get-cloud-queue").done(function (data) {
    var select = $("#cloud_files");
    for (var i = 0; i < data.length; i++) {
        var d = '<div class="k-block-2 file_selected" data-job_id="' + data[i].id + '" data-filename="' + data[i].filename + '">'
        d += '<div class="k-block-2__left"><div class="k-block-2__img-container"> </div> <p>' + data[i].filename + '</p> </div> </div>'
        select.append(d);
    }
}
);