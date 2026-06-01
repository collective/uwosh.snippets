/* global $, tinyMCEPopup, tinyMCE, tinymce, jQuery:false, document:false, window:false, location:false */

import registry from "@patternslib/patternslib/src/core/registry";
import utils from "@patternslib/patternslib/src/core/utils";

(function () {
  'use strict';

  var API_URL = $('body').attr('data-base-url') + '/@@snippets-api';

  var reOptions = {
    vocabularyUrl: $('body').attr('data-portal-url') + '/@@getVocabulary?name=plone.app.vocabularies.Catalog',
    maximumSelectionSize: 1
  };

  // load config
  $.ajax({
    url: API_URL,
    data: {
      action: 'configuration'
    }
  }).done(function(data){
    reOptions = $.extend({}, true, reOptions, JSON.parse(data.relatedItemsOptions));
  });

  function modalTemplate(context) {
    var template = '<div>' +
  '<h1>Add snippet</h1>' +
  '<div>' +
    '<div class="form-group snippets-content">' +
      '<label>Select content</label>' +
      '<input class="pat-contentbrowser" type="text"' +
            " data-pat-contentbrowser='__REOPTIONS__' />" +
    '</div>' +
    '<div class="form-group snippets-iframe">' +
      '<p>If snippet should display in an iframe, check this box, then specify a width and height</p>' +
      '<input type="checkbox" id="display-iframe" value="iframe" />' +
      '<label>Display in iframe?</label><br />' +
      '<label>iframe width:</label>' +
      '<input type="text" id="iframe-width" value="100%"/>' +
      '<label>iframe height:</label>' +
      '<input type="text" id="iframe-height" value="300px"/>' +
    '</div>' +
  '</div>' +
  '<div class="form-group snippets-section" style="display:none">' +
    '<label>Select section</label>' +
    '<span class="formHelp">You can select a particular section of the page to render.</span>' +
    '<select></select>' +
  '</div>' +
  '<div class="snippets-preview" style="display: none">' +
    '<h2>Snippet Preview</h2>' +
    '<div class="inner" style="padding: 10px;background: white;border: 1px solid #ccc;"></div>' +
  '</div>' +
  '<button class="plone-btn plone-btn-default cancel-btn">Cancel</button>' +
  '<button class="plone-btn plone-btn-primary insert-btn" disabled="true">Insert</button>' +
'</div>';

    return template.replace('__REOPTIONS__', context.reOptions);
  }

  tinymce.PluginManager.add('snippets', function (ed) {
      ed.on('init', function(){
        // make all existing not editable
        $('[data-type="snippet_tag"]', ed.getBody()).each(function(){
          this.setAttribute('contenteditable', false);
        });
      });

      function openSnippetWindow($node) {
        var $el = $('<div/>');
        $('body').append($el);
        var modal = registry.patterns["plone-modal"].init($el, {
          html: modalTemplate({
            reOptions: JSON.stringify(reOptions)
          }),
          content: null,
          buttons: '.plone-btn'
        });
        modal.on('shown', function() {
          var $re = $('input.pat-contentbrowser', modal.$modal);

          $re.on('change', function(){

            var value = (this && typeof this.value === 'string')
            if (!value) {
              return;
            }
            var data = this.value;
            if(data && data.length > 0){
              //utils.loading.show();
              $.ajax({
                url: API_URL,
                data: {
                  uid: data,
                  action: 'render'
                }
              }).done(function(data){
                $('.insert-btn', modal.$modal).removeAttr('disabled');
                var $els = $('<div>' + data.result + '</div>');
                $('.snippets-preview', modal.$modal).show();
                $('.snippets-preview .inner', modal.$modal).append($els);
                // parse to find headers...
                var headers = [];
                $('h1,h2,h3,h4,h5,h6', $els).each(function(){
                  headers.push($(this).text());
                });
                if(headers.length > 0){
                  var $sections = $('.snippets-section', modal.$modal);
                  $sections.show();
                  $('select', $sections).empty();
                  $('select', $sections).append($('<option value="">All</option>'));
                  headers.forEach(function(header){
                    var $option = $('<option value="' + header + '">' + header + '</option>');
                    $('select', $sections).append($option);
                  });
                }
              }).fail(function(){
                alert('error loading snippet data');
              }).always(function(){
              });
            }else{
              // clear out
              $('.snippets-preview', modal.$modal).hide();
              $('.snippets-section', modal.$modal).hide();
              $('.snippets-preview .inner', modal.$modal).empty();
              $('.insert-btn', modal.$modal).attr('disabled', 'true');
            }
          });

          $('.snippets-section select', modal.$modal).on('change', function(){
            var header = this.value;
            var data = this.value;
            if(data && data.length > 0){
              $.ajax({
                url: API_URL,
                data: {
                  uid: data,
                  action: 'render',
                  header: header
                }
              }).done(function(data){
                var $els = $('<div>' + data.result + '</div>');
                $('.snippets-preview .inner', modal.$modal).empty().append($els);
              });
            }
          });

          $('button', modal.$modal).off('click').on('click', function(){
            var $btn = $(this);
            if(!$btn.hasClass('insert-btn')){
              modal.hide();
              return;
            }

            var data = $re[0].value;
            var in_iframe = $('#display-iframe').is(':checked');
            var iframe_width = $('#iframe-width').val();
            var iframe_height = $('#iframe-height').val();
            if(data && data.length > 0){
              var header = $('.snippets-section select', modal.$modal).val();
              $.ajax({
                url: $('body').attr('data-base-url') + '/@@snippets-api',
                data: {
                  uid: data,
                  action: 'code',
                  header: header
                }
              }).done(function(resp){
                var attrs = {
                  class: 'snippet-tag snippet-tag-' + resp.result.toLowerCase().replace(' ', '-'),
                  'data-type': 'snippet_tag',
                  contenteditable: false,
                  'data-snippet-id': data,
                  'data-header': header,
                  'data-iframe': in_iframe,
                  'data-iframe-width': iframe_width,
                  'data-iframe-height': iframe_height,
                };
                if($node){
                  $node.attr(attrs);
                  $node.text(resp.result);
                }else{
                  ed.insertContent(ed.dom.createHTML('span', attrs, resp.result));
                }
              }).fail(function(){
                alert('error loading snippet data');
              }).always(function(){
                utils.loading.hide();
              });
            }
            modal.hide();
          });
        });
        modal.show();
      }

      ed.addCommand('snippets', function () {
        var $el = $(ed.selection.getNode());
        if($el.is('[data-type="snippet_tag"]')){
          openSnippetWindow($el);
        }else{
          openSnippetWindow();
        }
      });

      if (ed.ui && ed.ui.registry && ed.ui.registry.addButton) {
        ed.ui.registry.addButton('snippetbutton', {
          text: '{{}}',
          tooltip: 'Add snippet',
          onAction: function () {
            ed.execCommand('snippets');
          }
        });
      } else if (ed.addButton) {
        ed.addButton('snippetbutton', {
          cmd : 'snippets',
          image: $('body').attr('data-portal-url') + '/++resource++uwosh.snippets/brackets.png'
        });
      }
  });
}());
