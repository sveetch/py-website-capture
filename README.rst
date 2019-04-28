Website capture
===============

Actually a Proof of Concept for a tool able to take screenshot of many website
pages.

It implements some high level interface to take screenshot of full page.
Currently there is implementation with Selenium and another one with Splinter
(which act on top of Selenium) to test the two solutions.

Also there are some page on both solutions fails, like page which involve
some specific absolute position flows or have Javascript errors.

For now Splinter implementation seems to crop screenshots and Selenium
Webdriver allways have the better results. NOTE: Once you set a window size,
Splinter seems to be ok in fullscreen mode.

Also chromedriver at least in version 73 is bugged because screenshot is
largely cropped even if you enforce a window size, resulting image will have
something like 1/3 size less.

Goals
*****

An end user project with a command line interface using JSON for page registry
for screenshot tasks with responsive versions.

Also it should be a high level layer to implement custom code to perform tests
tasks on frontend (like event interaction, DOM inspection, etc..) since
Selenium and Splinter are ready for that.

Requires
********

* Python>=3.4;
* Virtualenv;
* Pip;
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

However in this way it will only usable as Python module, you won't have command line requirements.

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

    wget https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    sudo mv chromedriver /usr/local/bin
    rm -f chromedriver_linux64.zip

Links:

* `<http://chromedriver.chromium.org/>`_;
* `<https://pypi.org/project/selenium/#drivers>`_;

Going full headless
-------------------

Even interfaces have a ``headless`` mode, it only apply that browser are not
displayed when a Webdriver is performing request. You still need a common
desktop environment to run a browser which is not desirable on a server.

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

To launch screenshot tasks: ::

    website-capture screen --interface selenium --config sample.json

``--interface`` argument is not required but by default it use the dummy
interface which does not nothing, this is just for development debugging.
Available choices are ``dummy``, ``selenium`` and ``splinter``.

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
            },
            {
                "name": "google.com",
                "url": "https://www.google.com/",
                "sizes": [
                    [330, 768],
                    [1440, 768]
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
    is often odd. If needed you can add default size with value ``(0, 0)``.
filename
    Optional filename. When undefined, default behavior is to use the filename
    format from interface class that commonly contains size, page name and
    interface name. Filename can be formatted with some pattern according to
    page configuration. Like ``{name}``, ``{size}``, ``{url}``.

Todo
****

* Watch to get console logs from browser so we can log errors if any;
* Ensure accurate capture behavior with almost every websites;
* Test coverage for base stuff, we won't test real screenshoters which
  involves a real browser;
