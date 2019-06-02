# -*- coding: utf-8 -*-
import copy
import io
import json
import logging
import os

from selenium.common.exceptions import WebDriverException
from website_capture.exceptions import InvalidPageSizeError, PageConfigError


class BaseInterface(object):
    """
    Base screenshoter interface does not implement any driver, it's just a
    task runner for given page items.

    Keyword Arguments:
        headless (bool): Determine if browser is used through headless mode or
            not. Default is True
        basedir (string): Base directory where is save screenshot files.
        size_dir (string): Enable or not behavior to create a subdirectory for
            each different size used from page configurations. Default is True.
            Remember to add a size into template
            ``BaseInterface.DESTINATION_FILEPATH`` if you disable this and you
            have more than one size used in your pages.
    """
    DESTINATION_FILEPATH = "{name}_base.png"
    DRIVER_CLASS = None
    _default_size_value = (0, 0) # Do not change this
    AVAILABLE_PAGE_TASKS = {
        "screenshot": "task_screenshot",
        "logs": "task_logs",
    }

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
            not equal to empty size ``BaseInterface._default_size_value``,
            else return ``Default``.
        """
        size_repr = "Default"
        if (width, height) != self._default_size_value:
            size_repr = "{}x{}".format(width, height)

        return size_repr

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
        ``BaseInterface.DESTINATION_FILEPATH`` template may contains reference
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

        This is an extended version of page item options from configuration
        file with additional job context.
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
        config["driver_log_path"] = ".".join([config["destination"], "driver", "log"])
        config["browser_log_path"] = ".".join([config["destination"], "browser", "json"])

        return config

    def get_driver_options(self, config):
        """
        Should return available option object to pre configure your driver
        instance.
        """
        return {}

    def get_driver_class(self):
        """
        Return driver object class.
        """
        return self.DRIVER_CLASS

    def get_driver_instance(self, options, config):
        """
        Return driver instance pre configured with given config object.
        """
        msg = "Your 'BaseInterface' object must implement a driver."
        raise NotImplementedError(msg)

    def tear_down_driver(self, driver, config):
        """
        Implement this to close descriptor/pointer object after end of
        each ``BaseInterface.run()`` job, especially useful to close
        driver when page capture has been done.
        """
        self.log.debug("Closing driver")

    def set_browser_size(self, driver, config):
        """
        Should set browser window to given size from config.
        """
        pass

    def load_page(self, driver, config):
        """
        Load given page url into given driver
        """
        self.log.info("🔹 Getting page for: {} ({})".format(
            config["name"],
            self.get_size_repr(*config["size"]),
        ))

        return "Pretending to load page: {}".format(config["url"])

    def task_screenshot(self, driver, config, response):
        """
        Should screenshot loaded page.
        """
        return config["destination"]

    def task_logs(self, driver, config, response):
        """
        Should get browser logs from loaded page
        """
        return {}

    def capture(self, driver, config):
        """
        Perform screenshot with given driver for given page configuration.

        This should allways return path where screenshot file has been
        effectively writed to.
        """
        tasks = [task for task in config.get("tasks", []) if (task in self.AVAILABLE_PAGE_TASKS)]

        # Perform tasks if there is any valid ones
        if tasks:
            payload = {
                "name": config["name"],
                "url": config["url"],
                "size": config["size"],
            }

            response = self.load_page(driver, config)

            for task in tasks:
                payload[task] = getattr(
                    self,
                    self.AVAILABLE_PAGE_TASKS[task]
                )(driver, config, response)

            return payload
        # No valid task found
        else:
            self.log.warning("🔹 No enabled tasks for page: {} ({})".format(
                config["name"],
                self.get_size_repr(*config["size"]),
            ))
            return None

    def page_job(self, size, page):
        """
        Perform page job for given page with given size
        """
        built = []
        error_logs = []

        config = self.get_page_config(page, size)
        options = self.get_driver_options(config)
        driver = self.get_driver_instance(options, config)

        if size != self._default_size_value:
            self.set_browser_size(driver, config)

        try:
            payload = self.capture(driver, config)
        # Driver error is not critical to finish every jobs, it is
        # logged in and job queue continue
        except WebDriverException as e:
            self.tear_down_driver(driver, config)
            msg = ("Unable to reach page or unexpected error "
                    "with: {}")
            self.log.error(msg.format(config["url"]))
            self.log.error(e)
            error_logs.append({
                "name": config["name"],
                "url": config["url"],
                "size": size,
                "msg": msg,
                "error": e,
            })
        # Unexpected error kind is assumed to be critical
        except Exception as e:
            self.tear_down_driver(driver, config)
            raise e
        # Job succeed
        else:
            self.tear_down_driver(driver, config)
            if payload:
                built.append(payload)
                # Should live in dedicated task method
                if "screenshot" in payload:
                    self.log.debug("  - Saved screenshot to : {}".format(
                        config["destination"]
                    ))
                if "logs" in payload:
                    self.log.debug("  - Saved browser log to : {}".format(
                        config["browser_log_path"]
                    ))

        return built, error_logs

    def perform_size_pages(self, size, pages):
        """
        Perform page job for every page with given size
        """
        built = []
        error_logs = []

        # Create destination dir if not already exists
        sizedir = self.get_destination_dir(size)
        if not os.path.exists(sizedir):
            os.makedirs(sizedir)

        for page in pages:
            if size in page.get("sizes", [self._default_size_value]):
                paths, errors = self.page_job(size, page)
                built.extend(paths)
                error_logs.extend(errors)

        return built, error_logs

    def page_default_values(self, pages):
        """
        Patch page items with required default values for optional field
        """
        for page in pages:
            # If no sizes option or empty list, fill it with default size to
            # ensure they are processed
            if "sizes" not in page or ("sizes" in page and not page["sizes"]):
                page["sizes"] = [self._default_size_value]

        return pages

    def run(self, pages):
        """
        Proceed capture for every item
        """
        built = []
        error_logs = []

        pages = self.page_default_values(pages)
        available_sizes = self.get_available_sizes(pages)

        self.log.debug(f"Available sizes: {available_sizes}")
        for size in available_sizes:
            self.log.debug("Size: {}".format(self.get_size_repr(*size)))

            paths, errors = self.perform_size_pages(size, pages)
            built.extend(paths)
            error_logs.extend(errors)

        return built, error_logs


class LogManagerMixin:
    """
    A mixin for interface to get browser logs from driver logs.
    """
    def get_driver_logs_content(self, driver, config, response):
        """
        Get driver log content
        """
        with io.open(config["driver_log_path"], "r") as fp:
            content = fp.read()

        return content

    def remove_driver_logs(self, driver, config):
        """
        Will remove driver log file.

        You should call it only after driver has been closed.
        """
        if os.path.exists(config["driver_log_path"]):
            os.remove(config["driver_log_path"])

    def store_browser_logs(self, driver, config, payload):
        """
        Get driver log content
        """
        with io.open(config["browser_log_path"], "w") as fp:
            json.dump(payload, fp, indent=4)

        return config["browser_log_path"]

    def parse_logs(self, driver, config, content):
        """
        Should parse relevant logs from given content.
        """
        return []

    def task_logs(self, driver, config, response):
        """
        Store browser logs from driver logs.

        NOTE:
            Keep in mind that getting logs before closing driver won't be
            able to capture logs from "unload" browser events (like when a
            window is closed).
        """
        payload = {
            "name": config["name"],
            "url": config["url"],
            "size": config["size"],
        }

        content = self.get_driver_logs_content(driver, config, response)

        payload["logs"] = self.parse_logs(driver, config, content)

        return payload
