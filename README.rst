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

First you need to have Firefox browser installed.

This involves a sudo prompt: ::

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

First you need to have Chrome (or Chromium) browser installed.

This involves a sudo prompt: ::

    wget https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    sudo mv chromedriver /usr/local/bin
    rm -f chromedriver_linux64.zip

Links:

* `<http://chromedriver.chromium.org/>`_;
* `<https://pypi.org/project/selenium/#drivers>`_;

Install project
***************

::

    make install

Todo
****

* Watch to get console logs from browser so we can log errors if any;
* Use real logging, no ``print()`` anymore;
* Command line interface to use a screenshoter fed from a JSON file;
* Rethink capture with size dimension, since actually it perform
  a get of same url for each size, that is not really performant, (but
  maybe it's better to start again an interface instance to avoid bugs
  when resizing?);
* Test coverage for base stuff, we won't test real screenshoters which
  involves a real browser;
* Little documentation about procedure to go full headless with Xvfb so
  project could be used on a server;

  * `<http://elementalselenium.com/tips/38-headless>`_;
  * `<http://tobyho.com/2015/01/09/headless-browser-testing-xvfb/>`_;
  * `<https://github.com/ponty/pyvirtualdisplay>`_;
