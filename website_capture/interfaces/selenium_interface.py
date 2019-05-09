from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from website_capture.interfaces.base import BaseScreenshot

"""
TODO:
    We have a way to get browser logs (at least errors), not we have to manage
    them properly.

    Firefox seems hard to exploit for console.log but at least there is
    Javascript errors. Chrome should be more reliable for console.log.

    For both browsers, logs are saved to an unique file (depending from capture
    filename) that we will have to read and parse to collect useful stuff
    inside many browser level log (warning, errors from driver are also
    present). These log file may be removed optionally in the end of the
    capture process.

    Collected logs should be stored as JSON in a different and an unique file
    based on capture filename.

    To be clean, we need to separate screenshot job from log parsing in
    different optional method but still called (optionally) from capture()
    method. Then each page config should define what kind of job they require
    (screenshot, log, custom task??).
"""

class SeleniumFirefoxScreenshot(BaseScreenshot):
    """
    Using Firefox browser directly from WebDriver through Selenium.

    Here the interface is a browser driver.
    """
    DESTINATION_FILEPATH = "{name}_firefox_selenium.png"
    INTERFACE_CLASS = webdriver.Firefox

    def set_interface_size(self, interface, config):
        interface.set_window_size(*config["size"])

    def get_interface_options(self, config):
        options = FirefoxOptions()

        if self.headless:
            options.headless = True

        return {
            "options": options,
            "log_path": config["log_path"],
        }

    def get_interface_instance(self, options):
        klass = self.get_interface_class()
        interface = klass(**options)

        return interface

    def capture(self, interface, config):
        super().capture(interface, config)

        interface.get(config["url"])

        el = interface.find_element_by_tag_name('body')
        el.screenshot(config["destination"])

        return config["destination"]

    def tear_down_interface(self, interface):
        super().tear_down_interface(interface)
        interface.quit()


class SeleniumChromeScreenshot(SeleniumFirefoxScreenshot):
    """
    Using Chrome browser directly from WebDriver through Selenium.
    """
    DESTINATION_FILEPATH = "{name}_chrome_selenium.png"
    INTERFACE_CLASS = webdriver.Chrome

    def get_interface_options(self, config):
        options = ChromeOptions()
        if self.headless:
            options.headless = True

        return {
            "options": options,
            "service_log_path": config["log_path"],
        }

    def capture(self, interface, config):
        super().capture(interface, config)

        interface.get(config["url"])

        interface.get_screenshot_as_file(config["destination"])

        # The way to get log with chrome (not standardized by webdriver)
        #print(interface.get_log('browser'))

        return config["destination"]
