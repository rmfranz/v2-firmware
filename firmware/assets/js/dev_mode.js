$("#enable_ssh").on("click", function() {
    $.get("/ssh-enable");
});

$("#disable_ssh").on("click", function() {
    $.get("/ssh-disable");
});

$("#enable_dev_mode").on("click", function() {
    $.get("/enable-dev-mode");
});

$("#disable_dev_mode").on("click", function() {
    $.get("/disable-dev-mode");
});