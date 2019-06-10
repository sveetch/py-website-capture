.. _Optimus: https://github.com/sveetch/Optimus

=========
Page tests
=========

This is a sample website project to build some pages for testing
``py-website-capture`` with webdrivers against some cases.

Features
********

* Foundation 6.5.3;
* Sveetoy 0.8.0;
* Optimus 1.x;
* Virtualenv;
* Python3,
* Assets management,
* I18n translation catalogs.

Install
*******

This requires make, Python3, Virtualenv, Pip and C build toolchain to compile C modules.

::

    make install

Usage
*****

Just build everything : ::

    make build

Then run a basic HTTP server to see it: ::

    make run

This is just a quick way to start. There is much more available commands, see help for more details: ::

    make help

You should know than commonly to work on your templates and CSS in live, you will need to launch a watcher for templates, a watcher for Sass sources and a basic HTTP server, you will find these commands in Makefile help.

Overview
********

Optimus
    The static site builder used to build your project. Everything you need to know to manage page, project settings, assets and translations is on `Optimus documentation <https://optimus.readthedocs.org/>`_
Jinja
    Template syntax engine used in your page templates. `Jinja documentation <http://jinja.pocoo.org/docs/>`_.
CSS
    In this project it involves:

    * `Sass <https://sass-lang.com/>`_: the syntax used to write sources to build CSS stylesheets;
    * `Boussole <https://boussole.readthedocs.io/>`_: the tool used to build CSS from Sass sources;
    * `ITCSS <https://www.xfive.co/blog/itcss-scalable-maintainable-css-architecture/>`_: a structured methodology for Sass/CSS sources files used for shipped Sass sources;
Foundation for sites
    The front-end framework included in shipped Sass sources. `Foundation documentation <https://foundation.zurb.com/sites/docs/>`_.
Sveetoy
    A Sass library for programmatic rythm on top of Foundation for sites. `Sveetoy documentation <https://sveetch.github.io/Sveetoy/>`_.
