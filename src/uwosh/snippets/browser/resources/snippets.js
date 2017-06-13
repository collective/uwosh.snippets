/* global $, tinyMCEPopup, tinyMCE, tinymce, jQuery:false, document:false, window:false, location:false */

(function () {
  'use strict';

  var API_URL = $('body').attr('data-base-url') + '/@@snippets-api';

  var Modal = require('mockup-patterns-modal');
  var _ = require('underscore');
  var utils = require('mockup-utils');

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

  var ModaleTemplate = _.template('<div>' +
  '<h1>Add snippet</h1>' +
  '<div>' +
    '<div class="form-group snippets-content">' +
      '<label>Select content</label>' +
      '<input class="pat-relateditems" type="text"' +
            " data-pat-relateditems='<%= reOptions %>' />" +
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
'</div>');

  tinymce.create('tinymce.plugins.SnippetsPlugin', {

    init : function (ed) {

      ed.on('init', function(){
        // make all existing not editable
        $('[data-type="snippet_tag"]', ed.getBody()).each(function(){
          this.setAttribute('contenteditable', false);
        });
      });

      function openSnippetWindow($node) {
        var $el = $('<div/>');
        $('body').append($el);
        var modal = new Modal($el, {
          html: ModaleTemplate({
            reOptions: JSON.stringify(reOptions)
          }),
          content: null,
          buttons: '.plone-btn'
        });
        modal.on('shown', function() {
          var $re = $('input.pat-relateditems', modal.$modal);
          var re = $re.data('pattern-relateditems');

          // pay attention to browsing option
          if(re.options.browsing){
            re.browsing = re.options.browsing;
          }

          re.$el.on('change', function(){
            // populate preview and section list
            var data = re.$el.select2('data');
            if(data && data.length > 0){
              utils.loading.show();
              $.ajax({
                url: API_URL,
                data: {
                  uid: data[0].UID,
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
                utils.loading.hide();
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
            var data = re.$el.select2('data');
            if(data && data.length > 0){
              $.ajax({
                url: API_URL,
                data: {
                  uid: data[0].UID,
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

            var data = re.$el.select2('data');

            if(data && data.length > 0){
              utils.loading.show();
              var header = $('.snippets-section select', modal.$modal).val();
              $.ajax({
                url: $('body').attr('data-base-url') + '/@@snippets-api',
                data: {
                  uid: data[0].UID,
                  action: 'code',
                  header: header
                }
              }).done(function(resp){
                var attrs = {
                  class: 'snippet-tag snippet-tag-' + data[0].portal_type.toLowerCase().replace(' ', '-'),
                  'data-type': 'snippet_tag',
                  contenteditable: false,
                  'data-snippet-id': data[0].UID,
                  'data-header': header
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

      ed.addButton('snippetbutton', {
        cmd : 'snippets',
        image: $('body').attr('data-portal-url') + '/++resource++uwosh.snippets/brackets.png'
      });
    },
  });
  tinymce.PluginManager.add('snippets', tinymce.plugins.SnippetsPlugin);
}());
