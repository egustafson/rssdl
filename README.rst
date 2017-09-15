RSS-DL (Download) - Scan and download RSS artifacts
===================================================

Usage
-----

* `rssdl init` -- initialize the DB
* `rssdl add`  -- add a feed by href
* `rssdl rm`   -- remove a feed by feed_id
* `rssdl list` -- list feeds
* `rssdl update` -- fetch feed and update DB
* `rssdl dl`     -- download new content in a feed



Dev - Installation
------------------

    > virtualenv venv
    > source venv/bin/activate.csh     ## for (t)csh
    > rehash                           ## for (t)csh
    > pip install -r requirements.txt
    > python setup.py develop
    > rehash                           ## for (t)csh
    > rssdl --help

DB (re)initialization

    > cp rssdl.yaml-example rssdl.yaml
    #
    # edit rssdl.yam as appropriate -- defaults should be ok.
    #
    > rssdl init
    #
    # DB initialized
    #
    > rssdl add '<feed-url>'
    > rssdl list
      1: <feed-url>
    > rssdl update 1
    Success.
    > rssdl list 1
      1 [<timestamp>] 1st Article Title
      ...
      n [<timestamp>] nth Article Title
    >

Local user directory installation (install `requirements.txt`
somewhere):

    > python setup.py develop --user

See: https://setuptools.pypa.io/en/latest/setuptools.html#automatic-script-creation

This package uses Setuptools and prefers Python 3.


.. Local Variables:
.. mode: rst
.. End:
