(function() {
  tinymce.create('tinymce.plugins.SnippetsPlugin', {
    init : function(ed, url) {
      // Register the command so that it can be invoked by using tinyMCE.activeEditor.execCommand('mceExample');
            ed.addCommand('snippets', function(ui) {
                    alert('ey');
            });

            ed.addButton('snippetbutton', {
                    title : 'Add Snippet.',
                    cmd : 'snippets',
                    img : 'add-portlets.png',
            });
          }
  });
  tinymce.PluginManager.add('textsnippets', tinymce.plugins.SnippetsPlugin);
})();
