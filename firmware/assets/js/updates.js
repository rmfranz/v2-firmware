$("#update").on("click", function () {
  $('#updateModal').toggleClass("k-modal-overlay--visible");
  setTimeout(function () {
    $.ajax({
      url: "/make-update",
      success: function (result) {
        $('#updateModal').modal('hide');
      },
      async: false
    });
  }, 1000);
});

$("#update_modal_close").on("click", function () {
  $('#updateModal').toggleClass("k-modal-overlay--visible");
});