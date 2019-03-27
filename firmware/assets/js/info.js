var pressed = 0;
$('body').on('mousedown', function() {
    if(pressed == 10) {
        $('#dev_modal').toggleClass('k-modal-overlay--visible');
    }
    ++pressed;
})

$("#dev_modal_close").on("click", function() {
    $("#dev_modal").toggleClass( "k-modal-overlay--visible" );
});

$("#cancel_modal").on("click", function() {
    $("#dev_modal").toggleClass( "k-modal-overlay--visible" );
});