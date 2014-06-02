(function() {
  tinymce.create('tinymce.plugins.SnippetsPlugin', {
    init : function(ed, url) {

      tinymce.DOM.loadCSS(url + '/snippets.css');

      ed.addCommand('snippets', function(ui) {
        
        options = {
          current_url: url,
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

        //We just want to get each snippet once, if there are duplicates, just ignore them
        snippet_ids = [];
        $(snippets).each(function(index, item) {
          if( $.inArray($(item).attr('data-snippet-id'), snippet_ids) == -1 )
          {
            snippet_ids.push($(item).attr('data-snippet-id'));
          }
        });

        $(snippet_ids).each(function(index, item) {
          var edit_url = document.baseURI + '/@@get-snippet-list?json=true&snippet_id=';
          $.ajax({
            url: edit_url + item,
            dataType: 'json',
            success: function(data) {

              var snippet = $(tinyMCE.activeEditor.contentDocument).find('span[data-snippet-id="' + item + '"]');
              
              if( data == false )
              {
                var text = '<span data-type="dead_snippet"></span>'
                $(snippet).each(function()
                {
                  $(this).html(text);
                  $(this).css('display', 'none');
                });
              }
              else
              {            
                var text = data.text;
                $(snippet).each(function() {
                  $(this).html(text);
                  $(this).css('outline', 'black dotted thin');
                  $(this).css('display', 'inline-block');
                  $(this).addClass('no-select');
                  $(this).attr('contenteditable', 'false');
                });
              }
            },
            error: function(xhr) {
              console.log(xhr);
            },
          });
        });
      });
      ed.onPostProcess.add(function(ed, o) {
        var body = o.node;
        $(body).find('span[data-type="dead_snippet"]').parent().remove();
        $(body).find('span[data-type="snippet_tag"]').html("").removeAttr('contenteditable');


        o.content = $(body).html();
      });
      //Prevents TinyMCE from wrapping text in <p> tags. 
      //Since these are meant to be used in-line, 
      //breaking to a new paragraph obviously isn't desired.
      var pageUrl = String(document.URL);
      if( pageUrl.indexOf('@@edit-snippet') >= 0 || pageUrl.indexOf('@@create-snippet') >= 0)
      {
        ed.settings.force_p_newlines = 0;
        ed.settings.forced_root_block = false;
      }

      function openSnippetWindow(options)
      {
        ed.windowManager.open({
          file: url + '/@@get-snippet-list',
          width: 800,
          height: 700,
          inline: 1,
        }, options);
      }
    },
  });
  tinymce.PluginManager.add('snippets', tinymce.plugins.SnippetsPlugin);
})();
