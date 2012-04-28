bookie_parser
==========================
This is a split of some of the code in Bookie for doing the readable parsing
and (in the future) tag suggestion bits of Bookmarks. The idea is to spit this
out, make it useful, and also help make it a scalable bit of code on its own.

The plan is to use tornado to help do async url fetching of the content or
urls, parse it, and provide a JSON payload of data about the content in
return.

It should work where you give it a dump of html or you give it a url to fetch
on its own.

Once the readable bits are working we can work on adding in a tag
suggestion/hinting option as well.

I'd like to test this out by deploying to the Heroku cedar stack if possible,
so you might see some odd bits of things I have to add to make that work.


Installtion
------------
::

    $ sudo apt-get install python-dev librtmp-dev
    $ git clone git://github.com/mitechie/bookie_parser.git
    $ cd bookie_parser
    $ make


Running
--------
We use a local gunicorn server to server out the application. You can start
the server with

::

    $ make run
    $ make stop
