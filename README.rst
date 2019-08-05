Website capture
===============

A tool able to capture content from web pages.

It implements a high level interface to capture content (like screenshot,
logs, etc..) from a page the famous Selenium library.

Requires
********

* Python>=3.4;
* Virtualenv;
* Pip;
* `Selenium <https://pypi.org/project/selenium/>`_;
* A browser and its `WebDriver <https://developer.mozilla.org/en-US/docs/Web/WebDriver>`_;

Install
*******

Clone repository and install it as a project ::

    git clone https://github.com/sveetch/py-website-capture
    cd py-website-capture
    make install

``py-website-capture`` package is currently not released yet on Pypi so to
install it you will need to do something like: ::

    pip install git+https://github.com/sveetch/py-website-capture.git#egg=py_website_capture

However in this way it will only usable as Python module, you won't have
command line requirements.

To have command line working you will need to do instead: ::

    pip install git+https://github.com/sveetch/py-website-capture.git#egg=py_website_capture[cli]

Once done you may see below to install a working driver for required browsers.

Install drivers
***************

You will need to install a driver for browsers you want to use.

Depending on your browser version you may need to install a different driver
version, you may refer to the driver documentation to find information about
release and compatibility.

Commonly, driver have to be installed at level system in common binaries path
so it can be found automatically without to set an environment variable or
option.

Once installed on your system, you won't need to reinstall it again except if
your browser update to an incompatible version with installed driver.

geckodriver
-----------

You need to have Firefox browser installed.

Here is sample commands to quickly download and deploy driver on your system: ::

    wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
    tar xvzf geckodriver-v0.24.0-linux64.tar.gz
    chmod +x geckodriver
    sudo mv geckodriver /usr/local/bin
    rm -f geckodriver-v0.24.0-linux64.tar.gz

Links:

* `<https://firefox-source-docs.mozilla.org/testing/geckodriver/>`_;
* `<https://github.com/mozilla/geckodriver/releases>`_;
* `<https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu>`_;
* `<https://pypi.org/project/selenium/#drivers>`_;

chromedriver
------------

You need to have Chrome (or Chromium) browser installed.

Here is sample commands to quickly download and deploy driver on your system: ::

    wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    sudo mv chromedriver /usr/local/bin
    rm -f chromedriver_linux64.zip

Links:

* `<http://chromedriver.chromium.org/>`_;
* `<https://pypi.org/project/selenium/#drivers>`_;

Going full headless
-------------------

Even if drivers have a ``headless`` mode, it only imply that browser are not
displayed when a Webdriver is performing request. You will still need to have
a desktop environment to run a browser which is not desirable on a server.

To be able to use this project on a server you may look at ``Xvfb`` tool.

* `<https://en.wikipedia.org/wiki/Xvfb>`_;
* `<http://elementalselenium.com/tips/38-headless>`_;
* `<http://tobyho.com/2015/01/09/headless-browser-testing-xvfb/>`_;
* `<https://github.com/ponty/pyvirtualdisplay>`_;

Usage
*****

Command line interface
----------------------

Activate virtual environment: ::

    source .venv/bin/activate

Then you can call command line interface, for example to get programm
version: ::

    website-capture version

You may also directly reach the command line interface without to activate
virtual environment: ::

    .venv/bin/website-capture version

To read help about programm and available commands: ::

    website-capture -h

To read full help about a command, here the ``version`` command: ::

    website-capture version -h

To launch captures from a job configuration file ``sample.json``: ::

    website-capture capture --interface firefox --config sample.json

``--interface`` argument is not required but by default it use the dummy
interface which does not nothing, this is just for development debugging.
See ``capture`` command help to see available interfaces.

``--config`` argument is required and must be a path to an existing and valid
JSON configuration file.

Configuration file
------------------

A configuration file in JSON is required to perform tasks, it will contain
interface settings to use and pages to capture.

Here is a sample: ::

    {
        "output_dir": "/home/foo/outputs/",
        "size_dir": true,
        "headless": true,
        "pages": [
            {
                "name": "perdu.com",
                "url": "http://perdu.com/"
                "screenshot_method": "body",
                "processors": [
                    "website_capture.processors.DummyProcessor",
                    "website_capture.processors.ProcessorBase"
                ],
                "tasks": [
                    "processing",
                    "screenshot",
                    "report"
                ]
            },
            {
                "name": "google.com",
                "url": "https://www.google.com/",
                "sizes": [
                    [330, 768],
                    [1440, 768]
                ],
                "tasks": [
                    "screenshot"
                ]
            }
        ]
    }

output_dir
    Required path where files will be saved.
size_dir
    Optional boolean to enable or not to add size name as a subdirectory of
    ``output_dir`` when saving file according to the current size they are
    captured. Default behavior is to enable it.
headless
    Optional boolean to enable or not headless mode for interface, meaning
    when enabled the used browser won't display to your screen, if disabled
    browser will show during capture is performed, then it will automatically
    close once finished. Default behavior is to enable it.
pages
    List of page items to capture see next section for details.

Page item
.........

Each item must have a ``name`` and ``url``
values. Optionally you can define a ``sizes`` value which is a list of
window sizes to use during capture, every size will create a new file. This
is recommended since default size depend from interface and are often too
small.

Each item may have following options

name
    Required name to use to display in log for page and possibly used into
    filename destination.
url
    Required url to get to perform capture.
sizes
    Optional list of sizes which browser will adopts, each one will perform a
    new capture for given size. Each size is a list of two items respectively
    for width and height. If no sizes is defined the default size from driver
    is used, this is not recommanded since each driver has its own size which
    is often odd. If needed you can add default size with value ``[0, 0]``.
filename
    Optional filename to be used as base filepath for resulting files from
    task. Then each task will suffix this base filepath with its extension(s).

    When undefined, default behavior is to use the filename
    format from interface class that commonly contains size, page name and
    interface name. Filename can be formatted with some pattern according to
    page configuration. Like ``{name}``, ``{size}``, ``{url}``.
tasks
    A list of tasks to perform for this page. Available tasks are:

    * ``screenshot``: will create an image file of page screenshot;
    * ``processing`` will perform some tasks on page from additional modules;
    * ``report`` will create a JSON file to report captured logs from page;

    Although it's an optional argument, this is not really useful to define a
    page job without it since it won't do nothing except to initialize driver.

    Also the order does matter, ``report`` should always been the last item to
    be available to get every logs from possible previous tasks. ``screenshot``
    should be the first one if you don't use ``processing`` or if your
    processors don't alterate the page.
screenshot_method
    Optional method to perform screenshot. It can be either ``body`` or
    ``window``, default when not defined is ``body``.

    * ``body`` method will capture content from  ``<body>`` element, it means
      content are rendered from browser size but screenshot image will
      probably smaller or bigger than window size depending of content size;
    * ``window`` method will strictly respect browser size, if content is
      bigger it will be cutted out from screenshot and if bigger you will
      empty space in resulting image. You may also have window scrollbar added
      or removed from image depending content and browser.
processors
    A list of Python path to processor objects, they will be executed one after
    another given the page content (which could be altered by possible
    previous processors). Last part of path must be the processor object to run
    and everything before is the module(s) path to reach the object.


Processors
..........

**TODO: On current development**

Processors are objects to perform custom jobs you can code on your own.

Available ``processors`` are defined in page option as a list of Python paths
and their execution is enabled when ``processing`` is in the tasks list.

For example, this is the base processor: ::

    class ProcessorBase(object):
        """
        Basic processor don't do anything except exposing required methods
        signatures.

        Attributes:
            name (string): Processor name used to store its report datas or
                logging possible events. Each processor must have an unique name.
        """
        name = "basic"

        def __init__(self, *args, **kwargs):
            pass

        def run(self, driver, config, response):
            """
            This is where your processor should perform its work and possibly
            returns datas to append to processor reports which will be stored with
            processor name.
            """
            return None


Known issues
************

* Firefox report task is not able to get console logs, only Javascript errors;
* When doing a screenshot with ``body`` method with Chrome browser, if content
  width and height is bigger than browser size the horizontal scrollbar will be
  included at browser size bottom. This seems a bug of Chrome driver.

Development
***********

Project is developped with tests, for convenience they are splitted in two
distinct directory.

One to cover core interface which can be runned once project is installed
and one another dedicated to cover webdriver interfaces.

The last one will require you have installed every implemented drivers (and
their related browser) and running the demo server which you can find in
``page_tests`` directory, it have its own Makefile to install its requirements.
