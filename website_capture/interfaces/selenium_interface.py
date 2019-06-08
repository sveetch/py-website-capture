import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from website_capture.interfaces.base import BaseInterface, LogManagerMixin


class SeleniumFirefoxInterface(LogManagerMixin, BaseInterface):
    """
    Using Firefox browser directly from WebDriver through Selenium.

    Here the interface is a browser driver.
    """
    DESTINATION_FILEPATH = "{name}_firefox"
    DRIVER_CLASS = webdriver.Firefox
    FLUSH_DRIVER_LOGS = True # TODO: Should be overrided by page config option

    def set_browser_size(self, driver, config):
        driver.set_window_size(*config["size"])

    def get_driver_options(self, config):
        options = FirefoxOptions()

        if self.headless:
            options.headless = True

        # From Firefox 64 this should do the trick as last search result was
        # pointing it. Sadly it does not work, there is more search and tests
        # to do..
        fp = webdriver.FirefoxProfile()
        fp.set_preference("devtools.console.stdout.content", "true")

        # Update driver capabilities to ask for every browser logs so we have
        # errors and console.log
        dc = DesiredCapabilities.FIREFOX
        dc["loggingPrefs"] = {"browser": "ALL"}

        return {
            "options": options,
            # NOTE: Seems deprecated
            #"log_path": config["driver_log_path"],
            # NOTE: In profit of this one
            "service_log_path": config["driver_log_path"],
            "desired_capabilities": dc,
            "firefox_profile": fp,
        }

    def get_driver_instance(self, options, config):
        """
        Remove previous log file if exists (so it does not stack with logs
        from previous runs) then initialize driver.
        """
        if os.path.exists(config["driver_log_path"]):
            os.remove(config["driver_log_path"])

        klass = self.get_driver_class()
        driver = klass(**options)

        return driver

    def load_page(self, driver, config):
        super().load_page(driver, config)

        return driver.get(config["url"])

    def parse_logs(self, driver, config, content):
        """
        Parse browser logs from given content.

        For Javascript error we stand on idea that a relevant log is a line
        starting with a prefix which contains url since there can be local
        errors related to Gecko (or some other Firefox internal engine).

        Currently the state of browser logging is very difficult with Firefox,
        at least we are able to get Javascript issues (in a messy way) but
        getting "console.log" output is cryptic, see "get_driver_options"
        for much details.
        """
        logs = []
        error_prefix = "JavaScript error: {},".format(config["url"])

        for line in content.splitlines():
            if line.startswith(error_prefix):
                error = line[len(error_prefix):]
                logs.append(("error", error.strip()))

        return logs

    def task_report(self, driver, config, response):
        payload = super().task_report(driver, config, response)
        path = self.store_browser_logs(driver, config, payload)

        return path

    def task_screenshot(self, driver, config, response):
        """
        A trick with this driver is to select the body element to get it full,
        since default driver screenshot behavior will cut content to the
        window viewport (that should be the asked size from page config).
        """
        el = driver.find_element_by_tag_name("body")
        el.screenshot(config["screenshot_path"])

        return config["screenshot_path"]

    def tear_down_driver(self, driver, config):
        super().tear_down_driver(driver, config)

        if self.FLUSH_DRIVER_LOGS:
            self.remove_driver_logs(driver, config)

        driver.quit()


class SeleniumChromeInterface(SeleniumFirefoxInterface):
    """
    Using Chrome browser directly from WebDriver through Selenium.

    It is based on SeleniumFirefoxInterface since they share the Selenium
    base API.
    """
    DESTINATION_FILEPATH = "{name}_chrome"
    DRIVER_CLASS = webdriver.Chrome
    FLUSH_DRIVER_LOGS = True # TODO: Should be overrided by page config option

    def get_driver_options(self, config):
        options = ChromeOptions()
        if self.headless:
            options.headless = True

        # Update driver capabilities to ask for every browser logs so we have
        # errors and console.log
        dc = DesiredCapabilities.CHROME
        dc["loggingPrefs"] = {"browser": "ALL"}

        return {
            "options": options,
            "service_log_path": config["driver_log_path"],
            "desired_capabilities": dc,
        }

    def load_page(self, driver, config):
        super().load_page(driver, config)

        return driver.get(config["url"])

    def get_driver_logs_content(self, driver, config, response):
        """
        Chrome driver does not push logs to a file, but dispose them from its
        API
        """
        return driver.get_log("browser")

    def parse_logs(self, driver, config, content):
        """
        Parse browser logs from given content.

        For Javascript error we stand on idea that a relevant log is a line
        starting with a prefix which contains url since there can be local
        errors related to Gecko (or some other Firefox internal engine).
        """
        logs = []
        prefix = config["url"]

        for item in content:
            level = "info"
            msg = item["message"].strip()

            if item["level"] == "SEVERE":
                level = "error"

            if msg.startswith(prefix):
                msg = msg[len(prefix):]
            logs.append((level, msg.strip()))

        return logs

    def task_screenshot(self, driver, config, response):
        driver.get_screenshot_as_file(config["screenshot_path"])

        return config["screenshot_path"]

    def tear_down_driver(self, driver, config):
        super().tear_down_driver(driver, config)

        if self.FLUSH_DRIVER_LOGS:
            self.remove_driver_logs(driver, config)

        driver.quit()
