
$("#update").on("click", function () {
    $('#updateModal').toggleClass("k-modal-overlay--visible");
    $.get("/make-usb-update").done(function(data){
        if(data.error == 1) {
            $('#mount_error').toggleClass("initiallyHidden");
            $('#updateModal').toggleClass("k-modal-overlay--visible");
        } else if(data.error == 2) {
            $('#unmount_error').toggleClass("initiallyHidden");
            $('#updateModal').toggleClass("k-modal-overlay--visible");
        } else if(data.error == 3) {
            $('#download_error').toggleClass("initiallyHidden");
            $('#updateModal').toggleClass("k-modal-overlay--visible");
        } else if(data.error == 4) {
            $('#copy_unzip_error').toggleClass("initiallyHidden");
            $('#updateModal').toggleClass("k-modal-overlay--visible");
        } else if(data.error == 5) {
            $('#folder_error').toggleClass("initiallyHidden");
            $('#updateModal').toggleClass("k-modal-overlay--visible");
        }
    })
})