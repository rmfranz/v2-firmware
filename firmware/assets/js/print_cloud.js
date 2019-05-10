
$.get("/get-cloud-queue").done(function (data) {
    var resp = data.resp;
    var select = $("#cloud_files");
    if(resp == "error") {
        select.append('<h2 class="k-main__h2">Error with API</h2>');        
    } else if (resp.length) {
        select.append('<h2 class="k-main__h2">No files on queue</h2>');        
    } else {
        for (var i = 0; i < resp.length; i++) {
            var d = '<div class="k-block-2 file_selected" data-job_id="' + resp[i].id + '" >'
            d += '<div class="k-block-2__left"><div class="k-block-2__img-container"> </div> <p>' + resp[i].filename + '</p> </div> </div>'
            select.append(d);
        }
        $('.file_selected').click(function () {
            $("#wait_fetching_modal").toggleClass("k-modal-overlay--visible");    
            window.location.href = "/confirm-cloud-print?job_id=" + $(this).data('job_id');
        });
    }
    $("#waiting_info").toggleClass("initiallyHidden");
});
