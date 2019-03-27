$.get("/get-cloud-token").done(function (data) {
    $('#registration_code_btn').text(data.registration_code);
    $("#waiting_info").toggleClass("initiallyHidden");
    $("#registration_code").toggleClass("initiallyHidden");
});