/*jslint browser: true, bitwise: true, passfail: true, eqeq: true, newcap: true, plusplus: true, regexp: true, white: false, */
/*global alert, tinyMCEPopup, jQuery:false, document:false, window:false, location:false */

$(document).ready(function () {

  var t = tinyMCEPopup.getWindowArg('t');
  var setSelected = tinyMCEPopup.getWindowArg('setSelected');
  var snippet_reload = tinyMCEPopup.getWindowArg('reload');
  var selectedSnippet = $(t).find('#snippet-selection');

  function catchEdit() {
    var referrer = document.referrer;

    var match = referrer.match(/(\?|&)snippet-id=([a-zA-Z0-9\-]+)(&|$|)?/);

    if (match != null) {
      snippet_reload(match[2]);
    }
  }

  function sanitize(snippetId) {
    var snippet = snippetId.replace(/\./g, '\\.');
    snippet = snippet.replace(/\:/g, '\\:');

    return snippet;
  }

  function getSelectionElement() {
    //We need to do this the "hard" way because, when returning from
    //the snippet edit window, the t variable is nowhere to be found

    var windows = tinyMCEPopup.editor.windowManager.windows;
    var el, frame, doc;

    var objs = $.map(windows, function (value) {
      return [value];
    });

    $(objs).each(function (index) {

      el = objs[index].element.get();
      frame = $(el).find('iframe');
      doc = $(frame).contents();

      if ($(doc).find('#snippet-selection').length >= 1) {
        el = $(doc).find('#snippet-selection');
        return el;
      }
    });
  }

  function setPreviewWindow(snippet) {

    var type = typeof selectedSnippet;

    if (type == undefined) {
      selectedSnippet = getSelectionElement();
    }

    selectedSnippet.val(snippet);
    setSelected();
  }

  catchEdit();

  if (selectedSnippet.val() != "") {
    var selected = $(':radio[value="' + selectedSnippet.val() + '"]');
    $(selected).attr('checked', true);
    $(selected).addClass('highlight');
  }

  $('.snippet-box').each(function (even) {
    if (even % 2 == 0) {
      $(this).addClass('even');
    }
    even += 1;
  });

  $('#snippet-browser-cancel').click(function () {

    tinyMCEPopup.close();
  });

  $('#snippet-browser-select').click(function () {

    var current = $('input[name="snippet"]:checked').val();

    if (current == undefined) {
      tinyMCEPopup.editor.windowManager.alert('You much choose a snippet to select.');

    } else {

      current = sanitize(current);

      setPreviewWindow(current);
      tinyMCEPopup.close();
    }
  });

  $('.snippet-box').click(function () {

    $('.snippet-box').removeClass('highlight');
    $(this).find('input').attr('checked', true);
    $(this).addClass('highlight');
  });

  $('.snippet-box').mouseenter(function () {
    $(this).addClass('highlight');
  }).mouseleave(function () {
    if ($(this).find('input').attr('checked')) {
      return 0;
    }
    $(this).removeClass('highlight');
  });

  $('.snippet-delete').click(function (e) {
    e.preventDefault();
    var url = $(this);
    tinyMCEPopup.editor.windowManager.confirm("Are you sure you want to delete this snippet?", function (s) {
      if (s) {
        $.ajax({
          url: $(url).attr('href'),
          success: function (data) {
            if (data == 'True') {

              var doc = tinyMCEPopup.editor.contentDocument;
              var id = $(url).parent().find('.snippet-id').html();

              var plugs = $(doc).find('span[data-snippet-id="' + id + '"]');

              $(plugs).remove();
              tinyMCEPopup.editor.windowManager.alert("The snippet was deleted successfully.");
              $(url).parent().remove();

            } else {
              tinyMCEPopup.editor.windowManager.alert("Something when wrong. The snippet wasn't deleted: " + data);
            }
          }
        });
      } else {
        return false;
      }
    });
  });


});
