<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        <meta name="viewport" content="width=device-width" initial-scale="1.0">
        <title>Bookie: ${self.title()}</title>

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
       <div id="heading" class="yui3-u-1">
           <div class="logo">
               <a href="/" class="logo">Bookie</a>
               <span class="alt_logo">&nbsp;&#45; bookmark your web</span>
           </div>
           <a href="https://github.com/mitechie/bookie_parser">
               <img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png"
           alt="Fork me on GitHub"></a>
       </div>
        <div class="yui3-g-responsive">
            ${next.body()}
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
