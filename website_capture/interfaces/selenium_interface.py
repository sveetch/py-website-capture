from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from website_capture.interfaces.base import BaseScreenshot


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

        # TODO: We need to get file destination path here to use it to make
        # its own log file.

        if self.headless:
            options.headless = True

        return {
            "options": options,
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
        }

    def capture(self, interface, config):
        super().capture(interface, config)

        interface.get(config["url"])

        interface.get_screenshot_as_file(config["destination"])

        return config["destination"]
