
$.get("/get-update").done(function(data){
  if(data.error == "error"){  
    $("#waiting_info").toggleClass("initiallyHidden");
    $("#get_update_error").toggleClass("initiallyHidden");
  } else if(data.new == data.actual){
    $('#actual').text(data.actual);
    $("#waiting_info").toggleClass("initiallyHidden");
    $('#version_actual').toggleClass("initiallyHidden");
  } else if(!data.connectivity.startsWith("eth") && !data.connectivity.startsWith("wlan")) {
    $("#waiting_info").toggleClass("initiallyHidden");
    $("#no_connection").toggleClass("initiallyHidden");
  } else {
    $('#actual').text(data.actual);
    $('#new').text(data.new);    
    $("#waiting_info").toggleClass("initiallyHidden");
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

$("#repair_update").on("click", function () {
  $('#updateModal').toggleClass("k-modal-overlay--visible");
  $.get("/repair-update").done(function (data) {
    $("#get_update_error").toggleClass("initiallyHidden");
    $('#updateModal').toggleClass("k-modal-overlay--visible");
    $('#update_error').toggleClass("initiallyHidden");
  });
});

$("#update_modal_close").on("click", function () {
  $('#updateModal').toggleClass("k-modal-overlay--visible");
});