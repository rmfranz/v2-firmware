$('#jstree').jstree({
    'core' : {
      'data' : {
        'url' : '/listing-files/usb',
        'data' : function (node) {
          return { 'id' : 1 };
        }
      }
    }
});