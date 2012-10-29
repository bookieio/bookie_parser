<% from urlparse import urlparse %>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        <meta name="viewport" content="width=device-width" initial-scale="1.0">
        <title>Bookie: ${webpage.title}</title>
        <link rel="stylesheet"
            href="${request.static_url('bookie_parser:static/base.css')}"
            type="text/css" media="screen" charset="utf-8">
        <link rel="stylesheet"
            href="${request.static_url('bookie_parser:static/override.css')}"
            type="text/css" media="screen" charset="utf-8">
    </head>
    <body>
        <div class="readable">
            <div id="readable_content">
                <div class="heading">
                    <img class="favicon" alt="favicon"
                    src="http://s2.googleusercontent.com/s2/favicons?domain=${urlparse(webpage.url).netloc}" />
                    ${webpage.title}
                </div>
                ${webpage.readable|n}
            </div>
        </div>
        <div id="readable_data">
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
    </body>
</html>
