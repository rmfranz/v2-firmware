
$.get("/get-update").done(function(data){
  if(data.new == data.actual){
    $('#actual').text(data.actual)
    $('#version_actual').toggleClass("initiallyHidden");
  } else {
    $('#actual').text(data.actual);
    $('#new').text(data.new);    
    $('#version_new').toggleClass("initiallyHidden");
  }
});

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