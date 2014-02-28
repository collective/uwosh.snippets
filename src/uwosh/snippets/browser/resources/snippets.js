(function() {
  tinymce.create('tinymce.plugins.SnippetsPlugin', {
    init : function(ed, url) {

      tinymce.DOM.loadCSS(url + '/snippets.css');

      ed.addCommand('snippets', function(ui) {
        options = {
          current_url: url,
          editor_snippet: false,
        };
        openSnippetWindow(options);
      });

      ed.addButton('snippetbutton', {
        title : 'Add Snippet.',
        cmd : 'snippets',
      });

      ed.onClick.add(function(ed, e) {
          if( $(e.target).attr('data-type') == 'snippet_tag' )
          {
            snippet_element = e.target;

            options = {
              current_url: url,
              editor_snippet: snippet_element,
            };

            openSnippetWindow(options);
          }
      });

      ed.onLoadContent.add(function(ed, e) {
        var snippets = $(ed.contentDocument).find('span[data-type="snippet_tag"]');
        snippets.each(function() {

          var id = $(this).attr('data-snippet-id');

          var dataObj;

          $.getJSON('http://localhost:7000/Plone/@@get-snippet-list?json=true&snippet_id=' + id , function(data) {
            var text = data.text;
            var snippet = $(tinyMCE.activeEditor.contentDocument).find('span[data-snippet-id="' + id + '"]');

            $(snippet).text(text);
            $(snippet).css('outline', 'black dotted thin');
            $(snippet).css('display', 'inline-block');

          });

          var t = $('.snippet-plug')
        });
      });
      ed.onPostProcess.add(function(ed, o) {
        var regex = /<span\s*data-type="snippet_tag"\s*data-snippet-id="([a-zA-Z0-9_-]+?)"\s*>.+?<\/span>/

        var text = o.content;

        while( regex.test(text) )
        {
          var match = regex.exec(text);

          var tag = match[0]
          var id = match[1];

          var newTag = '<span data-type="snippet_tag" data-snippet-id="' + id + '"></span>';

          text = text.replace(tag, newTag);
        }

        o.content = text;
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

      function openSnippetWindow(options)
      {
        ed.windowManager.open({
          file: url + '/@@get-snippet-list',
          width: 600,
          height: 600,
          inline: 1,
        }, options);
      }
    },
  });
  tinymce.PluginManager.add('snippets', tinymce.plugins.SnippetsPlugin);
})();
