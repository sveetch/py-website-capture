# -*- coding: utf-8 -*-
import os
import copy
import logging

from selenium.common.exceptions import WebDriverException


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

    def set_interface_size(self, interface, size):
        """
        Should set interface window size if given size is not null (``0x0``).
        """
        pass

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

    def get_interface_config(self):
        """
        Should return available option object to pre configure your instance.
        """
        return {}

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

    def get_file_destination(self, interface, size, page):
        """
        Return screenshot file destination path.

        Given page item is passed to filename formating. So
        ``BaseScreenshot.DESTINATION_FILEPATH`` template may contains reference
        to item values like ``foo_{name}.png``. Ensure template only references
        values available for every page items.
        """
        context = copy.deepcopy(page)

        context.update({"size": size})

        return os.path.join(
            self.get_destination_dir(size),
            self.DESTINATION_FILEPATH.format(**context),
        )

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

    def tear_down_runner(self, interface, size, pages):
        """
        Implement this to close descriptor/pointer object after end of
        ``BaseScreenshot.run()`` jobs, especially useful to close interface
        when everything has been done.
        """
        self.log.info("Closing interface")

    def capture(self, interface, size, page):
        """
        Perform screenshot with given interface for given page item.

        This should allways return path where screenshot file has been
        effectively writed to.
        """
        if not page.get("name", None):
            msg = "Page configuration must have a 'name' value."
            raise KeyError(msg)
        if not page.get("url", None):
            msg = "Page configuration must have an 'url' value."
            raise KeyError(msg)

        self.log.info("🔹 Getting page for: {} ({})".format(
            page["name"],
            self.get_size_repr(*size),
        ))

        path = self.get_file_destination(interface, size, page)
        return path

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
                    raise ValueError(msg)

        return sorted(list(sizes))

    def run(self, pages):
        """
        Proceed screenshot for every item
        """
        config = self.get_interface_config()
        available_sizes = self.get_available_sizes(pages)

        self.log.debug(f"available_sizes: {available_sizes}")

        for size in available_sizes:
            self.log.debug("Size: {}".format(self.get_size_repr(*size)))

            # Create destination dir if not already exists
            sizedir = self.get_destination_dir(size)
            if not os.path.exists(sizedir):
                os.makedirs(sizedir)

            for page in pages:
                if size in page.get("sizes", [self._default_size_value]):
                    interface = self.get_interface_instance(config)
                    if size != self._default_size_value:
                        self.set_interface_size(interface, size)

                    try:
                        path = self.capture(interface, size, page)
                    except WebDriverException as e:
                        self.tear_down_runner(interface, size, pages)
                        msg = ("Unable to reach page or unexpected error "
                                "with: {}")
                        self.log.error(msg.format(page["url"]))
                        self.log.error(e)
                    except Exception as e:
                        self.tear_down_runner(interface, size, pages)
                        raise e
                    else:
                        self.tear_down_runner(interface, size, pages)
                        self.log.debug(f"  - Saved to : {path}")
