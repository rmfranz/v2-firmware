$("#update").on("click", function() {
    $('#updateModal').modal('show');
    $.ajax({url: "/make-update", 
      success: function(result){
        $('#updateModal').modal('hide');
      },
      async: false
    });
});

