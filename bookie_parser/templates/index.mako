<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        <meta name="viewport" content="width=device-width" initial-scale="1.0">
        <title>Bookie Readable Parsing</title>
        <link rel="stylesheet"
            href="${request.static_url('bookie_parser:static/grid.css')}"
            type="text/css" media="screen" charset="utf-8">
        <link rel="stylesheet"
            href="${request.static_url('bookie_parser:static/styles.css')}"
            type="text/css" media="screen" charset="utf-8">
        <link
            href='https://fonts.googleapis.com/css?family=Cabin|Cabin+Sketch:bold&v2'
            rel='stylesheet' type='text/css'/>
    </head>
    <body>
        <div class="yui3-g-responsive">

            <div id="heading" class="yui3-u-1">
                <div class="logo">
                    <a href="/" class="logo">Bookie</a>
                    <span class="alt_logo">&nbsp;&#45; bookmark your web</span>
                </div>
                <a href="https://github.com/mitechie/bookie_parser">
                    <img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png"
                alt="Fork me on GitHub"></a>
            </div>

            <article id="" class="yui3-u-1-2">
                <p>Welcome to the Bookie Readable Parser. This site provides an api
                for parsing the content of a web page and providing a clear and
                readable version of it.</p>
            </article>
            <article id="" class="yui3-u-1-2">
                <p>In the future we plan on adding additional logic to the application
                to help aid in selecting tags and other bits of metadata about the
                content.</p>
            </article>

            <article class="yui3-u-1-2">
                <h2>Try it out</h2>
                <form action="/view" method="GET" class="form">
                    <div>
                        <input type="text" name="url" placeholder="Enter Url..." />
                        <input type="submit" value="Read It" name="submit" />
                    </div>
                </form>
            </article>

            <article class="yui3-u-1-2">
                <h2>Bookmarklet</h2>
                <p>Drag this bookmarklet to your browser's bookmark bar and click on
                it when viewing a site you want to read in a clean way.</p>
                <div>
                    <a
                    title="View with Bookmark Parser" href="javascript:(function()
                    {location.href='http://r.bmark.us/view?url='+escape(location.href)}())">Read
                    with Bookie</a>
                </div>
            </article>

            <article class="yui3-u-1">
                <h2>Example</h2>
                <img src="/static/sample_readable_parser.png" alt="article parsed into a nice readable format." />
            </article>

            <article class="yui3-u-1">
                <h2>API</h2>
                <p>Example calls are shows using the <a href="">HTTPie</a> Python
                tool. It really makes testing out api calls and such a lot easer.</p>
            </article>

            <article class="yui3-u-1">
                <h3>Fetching URL Content</h3>
                <pre>$ http -j --follow  POST "http://127.0.0.1:6543/api/v1/parse" url="http://tornadoweb.org/documentation/httpclient.html#tornado.httpclient.AsyncHTTPClient.configure"</pre>
                <pre>

                HTTP/1.1 200 OK
                Content-Type: application/json; charset=UTF-8
                Etag: "d9eb34be9c858960e266571168419466ce423dba"
                Server: TornadoServer/2.2 (Gunicorn/0.14.2)
                Content-Length: 4812
                Connection: keep-alive

                {
                    "content": "&lt;html&gt;&lt;body/&gt;&lt;div id=\"content\"&gt;...&lt;/div&gt;\n&lt;/html&gt;",
                    "readable": {
                        "title": "Tornado Web Server",
                        "content": "...",
                        "hash_id": "...",
                        "readable": "...",
                        "request": {
                        }
                        "url": "tornadoweb.org/documentation/httpclient.html#tornado.httpclient.AsyncHTTPClient.configure"
                    }
                }
                </pre>
            </article>

            <article class="yui3-u-1">
                <h3>Viewing URL Content</h3>
                <pre>$ http -f GET "http://r.bmark.us/v?url=http://tornadoweb.org/documentation/httpclient.html#tornado.httpclient.AsyncHTTPClient.configure"</pre>
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
