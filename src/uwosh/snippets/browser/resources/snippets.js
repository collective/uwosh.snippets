(function() {
  tinymce.create('tinymce.plugins.SnippetsPlugin', {
    init : function(ed, url) {

      tinymce.DOM.loadCSS(url + '/snippets.css');
      // Register the command so that it can be invoked by using tinyMCE.activeEditor.execCommand('mceExample');
      ed.addCommand('snippets', function(ui) {
        ed.windowManager.open({
          file : url + '/@@get-snippet-list',
          width : 600,
          height : 600,
          inline : 1
        }, {
          current_url: url,
        });
      });

      ed.addButton('snippetbutton', {
        title : 'Add Snippet.',
        cmd : 'snippets',
      });

      //Prevents TinyMCE from wrapping text in <p> tags. 
      //Since these are meant to be used in-line, 
      //breaking to a new paragraph obviously isn't desired.
      if( String(document.URL).indexOf('.snippets') >= 0 )
      {
        ed.settings.force_p_newlines = 0;
        ed.settings.forced_root_block = false;
        //ed.settings.force_br_newlines = true;
      }
    }
  });
  tinymce.PluginManager.add('snippets', tinymce.plugins.SnippetsPlugin);
})();
