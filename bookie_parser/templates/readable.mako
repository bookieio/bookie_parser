<% from bookie_parser.lib.readable import urlparse %>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        <meta name="viewport" content="width=device-width" initial-scale="1.0">
        <title>Bookie: ${webpage.title}</title>
        <link rel="stylesheet"
            href="${request.static_url('bookie_parser:static/grid.css')}"
            type="text/css" media="screen" charset="utf-8">
        <link rel="stylesheet"
            href="${request.static_url('bookie_parser:static/styles.css')}"
            type="text/css" media="screen" charset="utf-8">
    </head>
    <body class="readable">
        <div class="readable-container">
        <article class="yui3-g-responsive">
            <div id="readable_content" class="yui3-u-1">
                <div class="heading">
                    <img class="favicon" alt="favicon"
                    src="http://s2.googleusercontent.com/s2/favicons?domain=${urlparse(webpage.url).netloc}" />
                    ${webpage.title}
                </div>
                ${webpage.readable|n}
            </div>
            <div id="readable_data" class="yui3-u-1">
                <ul>
                    <li>
                        <span class="data_label">Url:</span>
                        <a href="${webpage.url}">${webpage.url}</a>
                    </li>
                    <li>
                        <span class="data_label">Request Time:</span>
                        ${"{0:.3f}".format(webpage.request['request_time'])}
                    </li>
                </ul>
            </div>
        </article>
        </div>
        <script type="text/javascript">


          var _gaq = _gaq || [];
          _gaq.push(['_setAccount', '${request.registry.settings['google_analytics']}']);
          _gaq.push(['_trackPageview']);

          (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();

        </script>

    </body>
</html>
