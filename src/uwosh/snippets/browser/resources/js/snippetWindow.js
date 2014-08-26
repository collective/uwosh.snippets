/*jslint browser: true, bitwise: true, passfail: true, eqeq: true, newcap: true, plusplus: true, regexp: true, white: false, */
/*global alert, tinyMCEPopup, tinyMCE, jQuery:false, document:false, window:false, location:false */
$(document).ready(function () {

  document.title = 'Add a snippet';
  var t = $(this);

  var editor_snippet = tinyMCEPopup.getWindowArg('editor_snippet');

  function catchNestedSpans(plug) {

    //once in a while, the snippet-tag spans will
    //not get properly removed, so you'll have several nested
    //inside one another. This function gets the
    //upper-most of the 'snippet-plug' spans and returns it.

    if ($(plug).parent().attr('data-type') == 'snippet_tag') {
      plug = catchNestedSpans($(plug).parent());
    }

    return plug;
  }

  function getSelectedSnippet() {
    var selected = $('#snippet-selection').val();

    if (selected == "") {
      return "None";
    }

    selected = selected.replace(/\W/g, '');
    var id = '#snippet-' + selected;

    return $(id);
  }

  function getSelectedSnippetText() {

    var selected = getSelectedSnippet();

    if (selected == "None") {
      return "";
    }

    return $(selected).find('.snippet-text').html();
  }

  function setSelectedSnippet(selected) {

    var type = typeof selected;
    var snippet;

    if (type === 'undefined') {
      snippet = getSelectedSnippet();

    } else {
      snippet = selected;
      $('#snippet-selection').val($(snippet).find('.snippet-id').text());
    }

    if (snippet == "None") {
      $('#snippet-info-title').text('None');
      $('#snippet-desc').text('None');
      $('#snippet-info').show();
      return true;
    }

    if ($('#snippet-normal-buttons').css('display') != "none") {
      //We want to preserve all the formatting, so we use .html(), not .text()
      $('#snippet-preview').html($(snippet).find('.snippet-text').html());
    }

    $('#snippet-info-title').text($(snippet).find('.snippet-title').text());

    var snippetDesc = $(snippet).find('.snippet-description').text();
    var descText = "None";

    if (snippetDesc != "") {
      descText = snippetDesc;
    }

    $('#snippet-info-desc').text(descText);

    $('#snippet-info').show();
  }

  function fetchSnippet(snippetId) {
    var url = tinyMCEPopup.editor.documentBaseURI.source + '/@@get-snippet-list?json=true&snippet_id=';
    url += snippetId;

    $.ajax({
      url: url,
      dataType: 'json',
      success: function (responseText) {

        var response = '';

        if (typeof (responseText.id === undefined)) {
          response = responseText[0];

        } else {
          response = responseText;
        }

        var currentID = '#snippet-' + response.id;
        var item = $(currentID);
        setSelectedSnippet(item);
      },
    });
  }

  function catchNew() {
    //location.search returns anything after the ? in a URL
    var str = location.search;

    var newSnippet = str.match(/(\?|&)new_snippet=([a-zA-Z0-9_\-]+)(&|$|)?/);

    if (newSnippet != null) {
      var name = newSnippet[2];
      fetchSnippet(name);
    }
  }

  function createSpanElement(snippetId, snippetText) {
    var snippet = document.createElement('span');
    $(snippet).css('outline', "black dotted thin");
    $(snippet).css('display', 'inline-block');
    $(snippet).addClass('no-select');

    $(snippet).attr('data-type', 'snippet_tag');
    $(snippet).attr('data-snippet-id', snippetId);
    $(snippet).attr('contenteditable', 'false');

    $(snippet).html(snippetText);

    return snippet;
  }

  function createSpanTag(snippetId, snippetText) {
    if (snippetId != "") {
      var style = "outline-style: dotted; ";
      style += "outline-width: thin; ";
      style += "outline-color: black; ";
      style += "display: inline-block; ";
      return '<span style="' + style + '" class="no-select" contenteditable="false" data-type="snippet_tag" data-snippet-id="' + snippetId + '">' + snippetText + '</span>';
    }
  }

  function deletePlug(plug) {

    $(plug).remove();
  }

  function resetSnippet(responseText) {
    var id = responseText.id;
    var snippet = '#snippet-' + id;

    if ($(snippet).length <= 0) {
      return false;
    }

    $.each(responseText, function (k, v) {
      if (k == "id") {
        //continue
        return true;
      }

      var classname = '.snippet-' + k;

      if (k == 'text') {
        $(snippet).find(classname).html(v);

      } else {
        $(snippet).find(classname).text(v);
      }

    });

    if ($('#snippet-selection').val() == id) {
      setSelectedSnippet(snippet);
    }

    var doc = tinyMCEPopup.editor.dom.doc;

    $(doc).find('span[data-snippet-id="' + id + '"]').html(responseText.text);
  }

  function reload(snippetId) {
    var snippet = $(snippetId);
    var type = typeof snippet;

    if (type === undefined) {
      return false;
    }

    var url = tinyMCEPopup.editor.documentBaseURI.source + '/@@get-snippet-list?json=true&snippet_id=';
    url += snippetId;

    $.ajax({
      url: url,
      dataType: 'json',
      success: function (responseText) {
        resetSnippet(responseText[0]);
      }
    });
  }

  catchNew();

  if (editor_snippet !== undefined) {
    $('#snippet-selection').val($(editor_snippet).attr('data-snippet-id'));
    setSelectedSnippet();

    if (document.referrer.indexOf('/edit') > 0) {
      $('#snippet-delete').show();

    } else {

      $('#snippet-delete').hide();
    }
  } else {
    $('#snippet-delete').hide();
  }

  $('#snippet-create').click(function () {
    var url = tinyMCE.documentBaseURL;
    var doc = tinyMCE.DOM.doc;
    var body = $(doc).find('body');

    if ($('#snippet-create-link').length <= 0) {
      $(body).append('<a id="snippet-create-link" href="' + url + '@@create-snippet" class="overlay" style="display: none">Click me</a>');
    }

    $(body).attr('height', '800px').attr('width', '600px');

    $(body).find('#snippet-create-link').prepOverlay({
      subtype: 'iframe',
      cssclass: 'snippet-create-container',
      config: {top: '0%',
                    load: true,
                    oneinstance: false, },
    });
    $(body).find('.snippet-create-container iframe').attr('height', '700px').attr('width', '500px');
  });

  $('#snippet-delete').click(function () {
    tinyMCEPopup.editor.windowManager.confirm('Are you sure you want to remove the snippet plug from the current page?', function (s) {
      if (s) {
        deletePlug(editor_snippet);
        $('#snippet-delete').hide();

      } else {
        return true;
      }
    });
  });

  $('#snippet-insert').click(function () {
    var snippet = $('#snippet-selection').val();

    var text = getSelectedSnippet().find('.snippet-text').html();

    if (snippet != "None") {
      var output = createSpanElement(snippet, text);

      editor_snippet = tinyMCEPopup.getWindowArg('editor_snippet');

      if (editor_snippet != false && editor_snippet != undefined) {
        editor_snippet = catchNestedSpans(editor_snippet);
        //editor_snippet.parentElement.replaceChild(output, editor_snippet);
        $(editor_snippet).replaceWith(output);
        editor_snippet = false;
        tinyMCEPopup.close();
      }
      tinyMCEPopup.editor.selection.setContent($(output).prop('outerHTML').toString());

      tinyMCEPopup.close();

    } else if (snippet == undefined) {

      tinyMCEPopup.editor.windowManager.alert('You must select a snippet before saving.');
      $('#snippet-select').focus();
    }
  });

  $('#snippet-cancel').click(function () {

    tinyMCEPopup.close();
  });

  $('#snippet-view').click(function () {
    var body = tinyMCEPopup.editor.getDoc().body;
    $('#snippet-preview').html($(body).clone());
    $('#snippet-normal-buttons').hide();
    $('#snippet-preview-buttons').show();
  });

  $('#snippet-preview-cancel').click(function () {
    $('#snippet-normal-buttons').show();
    $('#snippet-preview-buttons').hide();
    $('#snippet-preview').html(getSelectedSnippetText());
  });

  $('#snippet-select').click(function () {
    $('#snippet-delete').hide();

    var url = tinyMCE.documentBaseURL;
    var ed = tinyMCE.activeEditor;
    ed.windowManager.open({
      file: url + '/@@get-snippet-list?list-view=true',
      width : 800,
      height : 600,
      inline : 1

    }, {
      t: t,
      setSelected: setSelectedSnippet,
      reload: reload,
    });
  });

  $('#snippet-preview-insert').click(function () {
    if ($('#snippet-selection').val() != "") {

      var text = getSelectedSnippet();
      var id = $(text).find('.snippet-id').text();
      text = $(text).find('.snippet-text').html();

      var snippet = createSpanTag(id, text);

      var preview = $('#snippet-preview').get(0);

      var sel = window.getSelection();
      var range = sel.getRangeAt(0);

      //makes sure the user selection is inside the
      //preview window. Otherwise, the user could replace
      //text anywhere on the window. Chaos ensues.
      if (range.intersectsNode(preview)) {
        if ($(range.startContainer.parentElement).attr('data-type') != 'snippet_tag') {
          sel.deleteFromDocument();
          range.insertNode($(snippet).get(0));

        } else {
          tinyMCEPopup.editor.windowManager.alert('Snippets cannot overlap. Please adjust your selection.');
        }
      } else {
        tinyMCEPopup.editor.windowManager.alert('You must select select a location to insert the snippet.');
      }
    } else {
      tinyMCEPopup.editor.windowManager.alert("You must select a snippet to insert.");
      $('#snippet-select').focus();
    }
  });

  $('#snippet-preview-save').click(function () {

    var body = $('#snippet-preview').contents();
    tinyMCEPopup.editor.setContent(body.html());

    tinyMCEPopup.close();
  });

});
