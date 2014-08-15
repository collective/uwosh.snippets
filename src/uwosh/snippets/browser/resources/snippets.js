/*jslint browser: true, bitwise: true, passfail: true, eqeq: true, newcap: true, plusplus: true, regexp: true, white: false, */
/*global alert, tinyMCEPopup, tinyMCE, tinymce, jQuery:false, document:false, window:false, location:false */

(function () {
  tinymce.create('tinymce.plugins.SnippetsPlugin', {
    init : function (ed, url) {

      function openSnippetWindow(options) {
        ed.windowManager.open({
          file: url + '/@@get-snippet-list',
          width: 800,
          height: 700,
          inline: 1,
        }, options);
      }

      tinymce.DOM.loadCSS(url + '/snippets.css');

      ed.addCommand('snippets', function () {

        var options = {
          current_url: url,
        };

        openSnippetWindow(options);
      });

      ed.addButton('snippetbutton', {
        title : 'Add Snippet.',
        cmd : 'snippets',
      });

      /*jslint unparam: true*/

      //Because the parameters are passed in a specified order, we need jsLint to ignore the unused 'ed' variable

      ed.onClick.add(function (ed, e) {
        if ($(e.target).parents('span[data-type="snippet_tag"]').length > 0 || $(e.target).attr('data-type') == 'snippet_tag') {
          var snippet_element;

          if ($(e.target).attr('data-type') == 'snippet_tag') {
            snippet_element = e.target;

          } else {
            snippet_element = $(e.target).parents('span[data-type="snippet_tag"]');
          }

          var options = {
            current_url: url,
            editor_snippet: snippet_element,
          };

          openSnippetWindow(options);
        }
      });
      /*jslint unparam: false*/

      ed.onSetContent.add(function (ed) {
        var snippets = $(ed.contentDocument).find('span[data-type="snippet_tag"]');

        //We just want to get each snippet once, if there are duplicates, just ignore them
        var snippet_ids = [];
        $(snippets).each(function (index) {
          if ($.inArray($(snippets[index]).attr('data-snippet-id'), snippet_ids) == -1) {
            snippet_ids.push($(snippets[index]).attr('data-snippet-id'));
          }
        });

        if (snippet_ids.length > 0) {

          var edit_url = document.baseURI + '/@@get-snippet-list?json=true&snippet_id=';

          var ids = [];
          $(snippet_ids).each(function (index) {
            ids.push(snippet_ids[index]);
          });

          var idList = ids.join();

          edit_url += idList;
          $.ajax({
            url: edit_url,
            dataType: 'json',
            success: function (data) {

              $(data).each(function () {

                var snippet = $(tinyMCE.activeEditor.contentDocument).find('span[data-snippet-id="' + this.id + '"]');

                var self = this;

                if (self.dead == true) {
                  var text = '<span data-type="dead_snippet"></span>';

                  $(snippet).each(function () {
                    $(this).html(text);
                    $(this).css('display', 'none');
                  });
                } else {
                  var output = self.text;
                  $(snippet).each(function () {
                    $(this).html(output);
                    $(this).css('outline', 'black dotted thin');
                    $(this).css('display', 'inline-block');
                    $(this).addClass('no-select');
                    $(this).attr('contenteditable', 'false');
                  });
                }
              });
            },
            error: function (xhr) {
              console.log(xhr);
            },
          });

        }
      });

      /*jslint unparam: true*/

      //Once again, the parameters are passed in a specific order here, so we need both of them,
      //even though "ed" is never used. Therefore, we tell jsLint to ignore that for now.
      ed.onPostProcess.add(function (ed, o) {
        var body = o.node;
        $(body).find('span[data-type="dead_snippet"]').parent().remove();
        var snippets = $(body).find('span[data-type="snippet_tag"]');

        $(snippets).html("").removeAttr('contenteditable');


        o.content = $(body).html();
      });

      /*jslint unparam: false*/

      //Prevents TinyMCE from wrapping text in <p> tags.
      //Since these are meant to be used in-line,
      //breaking to a new paragraph obviously isn't desired.
      var pageUrl = String(document.URL);

      if (pageUrl.indexOf('@@edit-snippet') >= 0 || pageUrl.indexOf('@@create-snippet') >= 0) {
        ed.settings.force_p_newlines = 0;
        ed.settings.forced_root_block = false;
        ed.settings.relative_urls = false;
        ed.settings.remove_script_host = true;
      }
    },
  });
  tinymce.PluginManager.add('snippets', tinymce.plugins.SnippetsPlugin);
}());
