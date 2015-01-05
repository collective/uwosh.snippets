/*jslint browser: true, bitwise: true, passfail: true, eqeq: true, newcap: true, plusplus: true, regexp: true, white: false, */
/*global alert, jQuery:false, document:false, window:false, location:false */

$(document).ready(function () {

  function close() {

    var before = window.location.href.indexOf('@@create-snippet');
    var urlBase = window.location.href.substr(0, before);
    var snippetWindow = "@@get-snippet-list";
    var snippetBrowserURI = "?list-view=true";

    var url = urlBase + snippetWindow;
    //This means we're editing a snippet.
    //We only want to pass the title back if it's a new snippet
    if ($('#form-widgets-id').val().length > 0) {
      window.location.href = url + snippetBrowserURI;
      return;
    }

    var id = $('#form-widgets-title').val();
    //Sanitize the id. It will be done again once it reaches the
    //form class, in case this fails (or the JS is subverted).
    id = id.replace(/\W/g, '');

    var form = $('#snippetIdForm');
    form.attr('action', url);

    if (id != "") {
      $(form).find('input').val(id);
    }

    form.submit();
  }

  $('#form-buttons-cancel').click(function (e) {
    e.preventDefault();
    close();
  });

  //Not sure why this is hidden to begin with, but lets
  //make it visible again.
  $('.suppressVisualEditor').css('margin', '0').show();
  $('.formControls').css('margin', '0');

  $('#form-buttons-save').click(function () {

    function successHandler() {
      alert('The snippet was saved successfully!');
      close();
    }

    var options = {
      success:   successHandler,
    };

    $('#form').ajaxForm(options);
  });
});
