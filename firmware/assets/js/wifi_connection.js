$.get("/get-wifi-connection").done(function (data) {
    var select = $("#wifi_list");
    var selected = data.selected;
    var wifi_list = data.wifi_list;
    if(wifi_list.length == 0) {
        select.append('<h2 class="k-main__h2">Error, try again</h2>');
    } else {
        for (var i = 0; i < wifi_list.length; i++) {
            var d = '<div data-wifiname="' + wifi_list[i] + '" class="k-block-2 wifi_selected">'
            d += '<div class="k-block-2__left"><p>'  + wifi_list[i] + '</p></div>'
            d += ' <div id="wifi_icons" class="k-block-2__right">'
            if(wifi_list[i] == selected) {
                d += '<img src="/static/images/icon-tilde_verde.svg" />'
            } else {
                d += '<img src="/static/images/icon_wifi-bloqueado.svg" />'
                d += '<img src="/static/images/icon_wifi-senal4.svg" />'
            }
            d += '</div>'
            select.append(d);
        }
        $('.wifi_selected').click(function () {
            var wifiname = $(this).data('wifiname');
            $("#network_name").val(wifiname);
            $("#network_name_title").text(wifiname);
            $('#wifi_modal').toggleClass('k-modal-overlay--visible');
        });
    }
    $("#waiting_info").toggleClass("initiallyHidden");
});


$("#cancel_modal").click(function () {
    $('#wifi_modal').toggleClass('k-modal-overlay--visible');
});

$("#confirm").click(function () {
    $("#wait_fetching_modal").toggleClass("k-modal-overlay--visible");
    var network_name = $("#network_name").val();
    var password = $("#keyboard").val();
    $.ajax({
        url: "/wifi-connection",
        method: "POST",
        data: {network_name: network_name, password: password},
        success: function (result) {
            if(network_name == result){
                $("#wait_fetching_modal").toggleClass("k-modal-overlay--visible");
                $("#connection_ok_modal").toggleClass("k-modal-overlay--visible");
            } else {
                $("#wait_fetching_modal").toggleClass("k-modal-overlay--visible");
                $("#connection_no_ok_modal").toggleClass("k-modal-overlay--visible");
            }
        }
    });
});

$("#connection_ok_modal_btn").click(function () {
    window.location.href = "/wifi-connection";
});

$("#connection_no_ok_modal_btn").click(function () {
    $("#connection_no_ok_modal").toggleClass("k-modal-overlay--visible");
});

$('#keyboard').keyboard({
  
    // set this to ISO 639-1 language code to override language set by the layout
    // http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    // language defaults to "en" if not found
    language: null, // string or array
    rtl: false, // language direction right-to-left

    // *** choose layout ***
    // layout: 'custom',
    // // customLayout: { 'normal': ['{cancel}'] },
    // customLayout: { 'normal': ['1 2 3 ', '4 5 6', '7 8 9', '{c} 0 {a}'] },
    // *** choose layout ***
    layout: 'custom',
    customLayout: {
'normal': [
    'q w e r t y u i o p',
    'a s d f g h j k l {bksp}',
    '{s} z x c v b n m , .',
    '{meta1} {space} {meta2} {accept}'
],
'shift': [
    'Q W E R T Y U I O P',
    'A S D F G H J K L {bksp}',
    '{s} Z X C V B N M ! ?',
    '{meta1} {space} {meta1} {accept}'
],
'meta1': [
    '1 2 3 4 5 6 7 8 9 0',
    '/ : ; ( ) \u20ac & @ {bksp}',
    '{meta2} - . , ? ! \' " {meta2}',
    '{normal} {space} {normal} {accept}'
],
'meta2': [
    '[ ] { } # % ^ * + = ',
    '_ \\ | ~ < > $ \u00a3 \u00a5 {bksp}',
    '{meta1} . , ? ! \' " {meta1}',
    '{normal} {space} {normal} {accept}'
]
},
    position: {
        // optional - null (attach to input/textarea) or a jQuery object
        // (attach elsewhere)
        of: null,
        my: 'center center',
        at: 'center center',
        // used when "usePreview" is false
        // (centers keyboard at bottom of the input/textarea)
        at2: 'center center'
    },

    // allow jQuery position utility to reposition the keyboard on window resize
    reposition: true,

    // preview added above keyboard if true, original input/textarea used if false
    // always disabled for contenteditable elements
    usePreview: true,

    // if true, the keyboard will always be visible
    alwaysOpen: false,

    // give the preview initial focus when the keyboard becomes visible
    initialFocus: true,
    // Avoid focusing the input the keyboard is attached to
    noFocus: false,

    // if true, keyboard will remain open even if the input loses focus.
    stayOpen: false,

    // Prevents the keyboard from closing when the user clicks or
    // presses outside the keyboard. The `autoAccept` option must
    // also be set to true when this option is true or changes are lost
    userClosed: false,

    // if true, keyboard will not close if you press escape.
    ignoreEsc: false,

    // if true, keyboard will only closed on click event instead of mousedown or
    // touchstart. The user can scroll the page without closing the keyboard.
    closeByClickEvent: false,

    // *** change keyboard language & look ***
    display: {
'bksp'   :  "<img src='/static/images/delete.png'>",
'accept' : 'return',
'normal' : 'ABC',
'meta1'  : '.?123',
'meta2'  : '#+=',
'accept'  : 'Enter'
},


    // Message added to the key title while hovering, if the mousewheel plugin exists
    wheelMessage: 'Use mousewheel to see other keys',

    css: {
    // input & preview
    // "label-default" for a darker background
    // "light" for white text
    input: 'form-control input-sm dark',
    // keyboard container
    container: 'center-block well',
    // default state
    buttonDefault: 'btn btn-default',
    // hovered button
    buttonHover: 'btn-primary',
    // Action keys (e.g. Accept, Cancel, Tab, etc);
    // this replaces "actionClass" option
    buttonAction: 'active',
    // used when disabling the decimal button {dec}
    // when a decimal exists in the input area
    buttonDisabled: 'disabled'
},

    // *** Useability ***
    // Auto-accept content when clicking outside the keyboard (popup will close)
    autoAccept: false,
    // Auto-accept content even if the user presses escape
    // (only works if `autoAccept` is `true`)
    autoAcceptOnEsc: false,

    // Prevents direct input in the preview window when true
    lockInput: false,

    // Prevent keys not in the displayed keyboard from being typed in
    restrictInput: false,
    // Additional allowed characters while restrictInput is true
    restrictInclude: '', // e.g. 'a b foo \ud83d\ude38'

    // Check input against validate function, if valid the accept button
    // is clickable; if invalid, the accept button is disabled.
    acceptValid: true,
    // Auto-accept when input is valid; requires `acceptValid`
    // set `true` & validate callback
    autoAcceptOnValid: false,

    // if acceptValid is true & the validate function returns a false, this option
    // will cancel a keyboard close only after the accept button is pressed
    cancelClose: true,

    // Use tab to navigate between input fields
    tabNavigation: false,

    // press enter (shift-enter in textarea) to go to the next input field
    enterNavigation: true,
    // mod key options: 'ctrlKey', 'shiftKey', 'altKey', 'metaKey' (MAC only)
    // alt-enter to go to previous; shift-alt-enter to accept & go to previous
    enterMod: 'altKey',

    // if true, the next button will stop on the last keyboard input/textarea;
    // prev button stops at first
    // if false, the next button will wrap to target the first input/textarea;
    // prev will go to the last
    stopAtEnd: true,

    // Set this to append the keyboard immediately after the input/textarea it
    // is attached to. This option works best when the input container doesn't
    // have a set width and when the "tabNavigation" option is true
    appendLocally: false,

    // Append the keyboard to a desired element. This can be a jQuery selector
    // string or object
    appendTo: 'body',

    // If false, the shift key will remain active until the next key is (mouse)
    // clicked on; if true it will stay active until pressed again
    stickyShift: false,

    // caret placed at the end of any text when keyboard becomes visible
    caretToEnd: false,

    // Prevent pasting content into the area
    preventPaste: false,

    // caret stays this many pixels from the edge of the input
    // while scrolling left/right; use "c" or "center" to center
    // the caret while scrolling
    scrollAdjustment: 10,

    // Set the max number of characters allowed in the input, setting it to
    // false disables this option
    maxLength: false,

    // allow inserting characters @ caret when maxLength is set
    maxInsert: true,

    // Mouse repeat delay - when clicking/touching a virtual keyboard key, after
    // this delay the key will start repeating
    repeatDelay: 500,

    // Mouse repeat rate - after the repeatDelay, this is the rate (characters
    // per second) at which the key is repeated. Added to simulate holding down
    // a real keyboard key and having it repeat. I haven't calculated the upper
    // limit of this rate, but it is limited to how fast the javascript can
    // process the keys. And for me, in Firefox, it's around 20.
    repeatRate: 20,

    // resets the keyboard to the default keyset when visible
    resetDefault: false,

    // Event (namespaced) on the input to reveal the keyboard. To disable it,
    // just set it to an empty string ''.
    openOn: 'focus',

    // When the character is added to the input
    keyBinding: 'mousedown touchstart',

    // enable/disable mousewheel functionality
    // enabling still depends on the mousewheel plugin
    useWheel: true,

    // combos (emulate dead keys)
    // http://en.wikipedia.org/wiki/Keyboard_layout#US-International
    // if user inputs `a the script converts it to à, ^o becomes ô, etc.
    useCombos: true,

    // *** Methods ***
    // Callbacks - add code inside any of these callback functions as desired
    initialized: function(e, keyboard, el) {},
    beforeVisible: function(e, keyboard, el) {$('.overlay').show();},
    visible: function(e, keyboard, el) {keyboard.$keyboard.addClass("in");},
    beforeInsert: function(e, keyboard, el, textToAdd) { return textToAdd; },
    change: function(e, keyboard, el) {},
    beforeClose: function(e, keyboard, el, accepted) {},
    accepted: function(e, keyboard, el) {},
    canceled: function(e, keyboard, el) {},
    restricted: function(e, keyboard, el) {},
    hidden: function(e, keyboard, el) {$('.overlay').hide();},

    // called instead of base.switchInput
    switchInput: function(keyboard, goToNext, isAccepted) {},

    // build key callback (individual keys)
    buildKey: function(keyboard, data) {
        /*
        data = {
          // READ ONLY
          // true if key is an action key
          isAction : [boolean],
          // key class name suffix ( prefix = 'ui-keyboard-' ); may include
          // decimal ascii value of character
          name     : [string],
          // text inserted (non-action keys)
          value    : [string],
          // title attribute of key
          title    : [string],
          // keyaction name
          action   : [string],
          // HTML of the key; it includes a <span> wrapping the text
          html     : [string],
          // jQuery selector of key which is already appended to keyboard
          // use to modify key HTML
          $key     : [object]
        }
        */
        return data;
    },

    // this callback is called just before the "beforeClose" to check the value
    // if the value is valid, return true and the keyboard will continue as it
    // should (close if not always open, etc)
    // if the value is not value, return false and the clear the keyboard value
    // ( like this "keyboard.$preview.val('');" ), if desired
    // The validate function is called after each input, the "isClosing" value
    // will be false; when the accept button is clicked, "isClosing" is true
    validate: function(keyboard, value, isClosing) {
        return true;
    }

});