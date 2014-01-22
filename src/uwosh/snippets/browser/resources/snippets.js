(function() {
  tinymce.create('tinymce.plugins.SnippetsPlugin', {
    init : function(ed, url) {

      tinymce.DOM.loadCSS(url + '/snippets.css');
      // Register the command so that it can be invoked by using tinyMCE.activeEditor.execCommand('mceExample');
            ed.addCommand('snippets', function(ui) {
                ed.windowManager.open({
                    file : url + '/@@get-snippet-list',
                    width : ed.getParam('template_popup_width', 500),
                    height : ed.getParam('template_popup_height', 500),
                    inline : 1
                });
            });

            ed.addButton('snippetbutton', {
                    title : 'Add Snippet.',
                    cmd : 'snippets',
            });
          }
  });
  tinymce.PluginManager.add('snippets', tinymce.plugins.SnippetsPlugin);
})();
