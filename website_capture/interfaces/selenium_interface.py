import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from website_capture.interfaces.base import BaseScreenshot, LogManagerMixin


class SeleniumFirefoxScreenshot(LogManagerMixin, BaseScreenshot):
    """
    Using Firefox browser directly from WebDriver through Selenium.

    Here the interface is a browser driver.
    """
    DESTINATION_FILEPATH = "{name}_firefox_selenium.png"
    INTERFACE_CLASS = webdriver.Firefox
    FLUSH_DRIVER_LOGS = True # TODO: Should be override by page config option

    def set_interface_size(self, interface, config):
        interface.set_window_size(*config["size"])

    def get_interface_options(self, config):
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
            "log_path": config["interface_log_path"],
            "desired_capabilities": dc,
            "firefox_profile": fp,
        }

    def get_interface_instance(self, options, config):
        """
        Remove previous log filename if exists (so it does stack with logs
        from previous runs) then initialize interface.
        """
        if os.path.exists(config["interface_log_path"]):
            os.remove(config["interface_log_path"])

        klass = self.get_interface_class()
        interface = klass(**options)

        return interface

    def load_page(self, interface, config):
        super().load_page(interface, config)

        return interface.get(config["url"])

    def parse_logs(self, interface, config, content):
        """
        Parse browser logs from given content.

        For Javascript error we stand on idea that a relevant log is a line
        starting with a prefix which contains url since there can be local
        errors related to Gecko (or some other Firefox internal engine).

        Currently the state of browser logging is very difficult with Firefox,
        at least we are able to get Javascript issues (in a messy way) but
        getting "console.log" output is cryptic, see "get_interface_options"
        for much details.
        """
        logs = []
        error_prefix = "JavaScript error: {},".format(config["url"])

        for line in content.splitlines():
            if line.startswith(error_prefix):
                error = line[len(error_prefix):]
                logs.append(("error", error.strip()))

        return logs

    def task_logs(self, interface, config, response):
        payload = super().task_logs(interface, config, response)
        self.store_browser_logs(interface, config, payload)

        return payload

    def task_screenshot(self, interface, config, response):
        """
        A trick with this driver is to select the body element to get it full,
        since default driver screenshot behavior will cut content to the
        window viewport (that should be the asked size from page config).
        """
        el = interface.find_element_by_tag_name("body")
        el.screenshot(config["destination"])

        return config["destination"]

    def tear_down_interface(self, interface, config):
        super().tear_down_interface(interface, config)

        if self.FLUSH_DRIVER_LOGS:
            self.remove_driver_logs(interface, config)

        interface.quit()


class SeleniumChromeScreenshot(SeleniumFirefoxScreenshot):
    """
    Using Chrome browser directly from WebDriver through Selenium.

    It is based on SeleniumFirefoxScreenshot since they share the Selenium
    base API.
    """
    DESTINATION_FILEPATH = "{name}_chrome_selenium.png"
    INTERFACE_CLASS = webdriver.Chrome
    FLUSH_DRIVER_LOGS = True # TODO: Should be override by page config option

    def get_interface_options(self, config):
        options = ChromeOptions()
        if self.headless:
            options.headless = True

        # Update driver capabilities to ask for every browser logs so we have
        # errors and console.log
        dc = DesiredCapabilities.CHROME
        dc["loggingPrefs"] = {"browser": "ALL"}

        return {
            "options": options,
            "service_log_path": config["interface_log_path"],
            "desired_capabilities": dc,
        }

    def load_page(self, interface, config):
        super().load_page(interface, config)

        return interface.get(config["url"])

    def get_driver_logs_content(self, interface, config, response):
        """
        Chrome driver does not push logs to a file, but dispose them from its
        API
        """
        return interface.get_log("browser")

    def parse_logs(self, interface, config, content):
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

    def task_screenshot(self, interface, config, response):
        interface.get_screenshot_as_file(config["destination"])

        return config["destination"]

    def tear_down_interface(self, interface, config):
        super().tear_down_interface(interface, config)

        if self.FLUSH_DRIVER_LOGS:
            self.remove_driver_logs(interface, config)

        interface.quit()
