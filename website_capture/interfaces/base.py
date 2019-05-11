# -*- coding: utf-8 -*-
import os
import copy
import logging

from selenium.common.exceptions import WebDriverException
from website_capture.exceptions import InvalidPageSizeError, PageConfigError


class BaseScreenshot(object):
    """
    Base screenshoter interface does not implement any interface, it's just a
    task runner for given page items.

    Keyword Arguments:
        headless (bool): Determine if browser is used through headless mode or
            not. Default is True
        basedir (string): Base directory where is save screenshot files.
        size_dir (string): Enable or not behavior to create a subdirectory for
            each different size used from page configurations. Default is True.
            Remember to add a size into template
            ``BaseScreenshot.DESTINATION_FILEPATH`` if you disable this and you
            have more than one size used in your pages.
    """
    DESTINATION_FILEPATH = "{name}_base.png"
    INTERFACE_CLASS = None
    _default_size_value = (0, 0) # Do not change this

    def __init__(self, basedir="", headless=True, size_dir=True):
        self.headless = headless
        self.basedir = basedir
        self.size_dir = size_dir
        self.log = logging.getLogger("py-website-capture")

    def get_available_sizes(self, pages):
        """
        Walk on every page items to find all distinct sizes they require.
        """
        sizes = set([self._default_size_value])

        for page in pages:
            for item in page.get("sizes", []):
                try:
                    width, height = item
                    sizes.add((width, height))
                except ValueError:
                    msg = ("Invalid size value, it should be a tuple of "
                            "exactly two integers "
                            "(width, height): {}").format(item)
                    raise InvalidPageSizeError(msg)

        return sorted(list(sizes))

    def get_size_repr(self, width, height):
        """
        Return size representation.

        Arguments:
            width (int): Positive width value.
            height (int): Positive Height value.

        Return:
            string: Size representation such as ``WIDTHxHEIGHT`` if size is
            not equal to empty size ``BaseScreenshot._default_size_value``,
            else return ``Default``.
        """
        size_repr = "Default"
        if (width, height) != self._default_size_value:
            size_repr = "{}x{}".format(width, height)

        return size_repr

    def set_interface_size(self, interface, config):
        """
        Should set interface window size if given page size is not
        null (``0x0``).
        """
        pass

    def get_destination_dir(self, size):
        """
        Return base directory for screenshot file.
        """
        if not self.size_dir:
            return self.basedir

        return os.path.join(
            self.basedir,
            self.get_size_repr(*size)
        )

    def get_file_destination(self, config):
        """
        Return screenshot file destination path.

        Given page item is passed to filename formating. So
        ``BaseScreenshot.DESTINATION_FILEPATH`` template may contains reference
        to item values like ``foo_{name}.png``. You must ensure template only
        references values available for every page items.
        """
        filename = config.get("filename", self.DESTINATION_FILEPATH)

        return os.path.join(
            self.get_destination_dir(config["size"]),
            filename.format(**config),
        )

    def get_page_config(self, page, size):
        """
        Validate and return page configuration.

        Base configuration is given page item plus some additional context.
        """
        if not page.get("name", None):
            msg = "Page configuration must have a 'name' value."
            raise PageConfigError(msg)

        if not page.get("url", None):
            msg = "Page configuration must have an 'url' value."
            raise PageConfigError(msg)

        config = copy.deepcopy(page)

        config["size"] = size

        config["destination"] = self.get_file_destination(config)
        config["log_path"] = ".".join([config["destination"], "driver", "log"])

        return config

    def get_interface_options(self, config):
        """
        Should return available option object to pre configure your instance.
        """
        return {}

    def get_interface_class(self):
        """
        Return interface object class.
        """
        return self.INTERFACE_CLASS

    def get_interface_instance(self, config):
        """
        Return interface instance pre configured with given config object.
        """
        msg = "Your 'BaseScreenshot' object must implement an interface"
        raise NotImplementedError(msg)

    def capture(self, interface, config):
        """
        Perform screenshot with given interface for given page configuration.

        This should allways return path where screenshot file has been
        effectively writed to.

        TODO:
            * Capture browser console logs (errors, warnings, etc.. occuring
              during page loading/rendering, not driver, etc.. logs) in an
              optional file. Need tests on various behavior with some dummy
              pages to reproduce cases.
            * Start moving screenshot code into its own method, so capture stay
              as "a capture theses things from page" and cut "things" into
              individual methods so we can choose what thing jobs to perform;
        """
        self.log.info("🔹 Getting page for: {} ({})".format(
            config["name"],
            self.get_size_repr(*config["size"]),
        ))

        return config["destination"]

    def tear_down_interface(self, interface):
        """
        Implement this to close descriptor/pointer object after end of
        each ``BaseScreenshot.run()`` job, especially useful to close
        interface when page capture has been done.
        """
        self.log.debug("Closing interface")

    def run(self, pages):
        """
        Proceed screenshot for every item
        """
        built = []

        available_sizes = self.get_available_sizes(pages)

        self.log.debug(f"Available sizes: {available_sizes}")
        for size in available_sizes:
            self.log.debug("Size: {}".format(self.get_size_repr(*size)))

            # Create destination dir if not already exists
            sizedir = self.get_destination_dir(size)
            if not os.path.exists(sizedir):
                os.makedirs(sizedir)

            for page in pages:
                if size in page.get("sizes", [self._default_size_value]):
                    config = self.get_page_config(page, size)
                    options = self.get_interface_options(config)
                    interface = self.get_interface_instance(options)

                    if size != self._default_size_value:
                        self.set_interface_size(interface, config)

                    try:
                        path = self.capture(interface, config)
                    except WebDriverException as e:
                        self.tear_down_interface(interface)
                        msg = ("Unable to reach page or unexpected error "
                                "with: {}")
                        self.log.error(msg.format(config["url"]))
                        self.log.error(e)
                    except Exception as e:
                        self.tear_down_interface(interface)
                        raise e
                    else:
                        built.append(path)
                        self.log.debug(f"  - Saved to : {path}")
                        self.tear_down_interface(interface)
        return built
