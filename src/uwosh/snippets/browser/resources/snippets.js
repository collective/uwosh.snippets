/* global $, tinyMCEPopup, tinyMCE, tinymce, jQuery:false, document:false, window:false, location:false */

(function () {
  'use strict';

  var Modal = require('mockup-patterns-modal');
  var _ = require('underscore');

  var reOptions = {
    vocabularyUrl: $('body').attr('data-portal-url') + '/@@getVocabulary?name=plone.app.vocabularies.Catalog',
    maximumSelectionSize: 1
  };

  var ModaleTemplate = _.template('<div>' +
  '<h1>Add snippet</h1>' +
  '<div>' +
    '<div class="form-group">' +
      '<label>Select content</label>' +
      '<input class="pat-relateditems" type="text"' +
            " data-pat-relateditems='" + JSON.stringify(reOptions) + "' />" +
    '</div>' +
  '</div>' +
  '<button class="plone-btn plone-btn-default cancel-btn">Cancel</button>' +
  '<button class="plone-btn plone-btn-primary insert-btn">Insert</button>' +
'</div>');

  tinymce.create('tinymce.plugins.SnippetsPlugin', {
    init : function (ed, url) {

      function openSnippetWindow() {
        var $el = $('<div/>');
        $('body').append($el);
        var modal = new Modal($el, {
          html: ModaleTemplate(),
          content: null,
          buttons: '.plone-btn'
        });
        modal.on('shown', function() {
          $('button', modal.$modal).off('click').on('click', function(){
            var $btn = $(this);
            if(!$btn.hasClass('insert-btn')){
              return;
            }
            var $re = $('input.pat-relateditems', modal.$modal);
            var re = $re.data('pattern-relateditems');
            var data = re.$el.select2('data');

            if(data && data.length > 0){
              ed.insertContent(ed.dom.createHTML('span', {
                'data-type': 'snippet_tag',
                contenteditable: "false",
                'data-snippet-id': data[0].UID
              }, 'Snippet'));
            }
            modal.hide();
          });
        });
        modal.show();
      }

      ed.addCommand('snippets', function () {
        openSnippetWindow();
      });

      ed.addButton('snippetbutton', {
        text : 'Add Snippet',
        cmd : 'snippets',
      });
    },
  });
  tinymce.PluginManager.add('snippets', tinymce.plugins.SnippetsPlugin);
}());
