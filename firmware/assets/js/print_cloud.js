
$.get("/get-cloud-queue").done(function (data) {
    var resp = data.resp;
    var select = $("#cloud_files");
    if(resp == "error") {
        select.append('<h2 class="k-main__h2">Error with API</h2>');        
    } else if (resp.length == 0) {
        select.append('<h2 class="k-main__h2">No files on queue</h2>');        
    } else {
        for (var i = 0; i < resp.length; i++) {
            var totalSeconds = resp[i].printing_duration;
            var hours = Math.floor(totalSeconds / 3600);
            totalSeconds %= 3600;
            var minutes = Math.floor(totalSeconds / 60);
            var d = '<div class="k-block-2 file_selected" data-job_id="' + resp[i].id + '" >'
            d += '<div class="k-block-2__left"><div class="k-block-2__img-container"> <img src="'+ resp[i].preview_image +'.png.square.png" style="height: 64px" />'
            d += ' </div> <p>' + resp[i].filename.split(".gcode")[0] + '</p> '
            d += ' </div> <div class="k-block-2__right"><p> ' + hours +'h ' + minutes + 'm </p></div> </div>'
            select.append(d);
        }
        $('.file_selected').click(function () {
            $("#wait_fetching_modal").toggleClass("k-modal-overlay--visible");    
            window.location.href = "/confirm-cloud-print?job_id=" + $(this).data('job_id');
        });
    }
    $("#waiting_info").toggleClass("initiallyHidden");
});
