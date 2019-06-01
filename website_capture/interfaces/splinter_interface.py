"""
DEPRECATED
"""
from splinter import Browser

from website_capture.interfaces.base import BaseInterface


class SplinterFirefoxScreenshot(BaseInterface):
    """
    Using Firefox browser through Splinter interface which is a layer on top
    of WebDriver through Selenium.

    Here the interface is the Splinter "browser" object.

    NOTE: Not up to date with last Interface API, may be removed since Splinter
    is buggy on screenshot and may useful anymore.
    """
    DESTINATION_FILEPATH = "{name}_firefox_splinter.png"
    BROWSER_TYPE = "firefox"

    def set_browser_size(self, interface, config):
        interface.driver.set_window_size(*config["size"])

    def get_driver_options(self, config):
        options = {}

        if self.headless:
            options["headless"] = True

        options["log_path"] = config["log_path"]

        return options

    def get_driver_instance(self, options):
        return Browser(self.BROWSER_TYPE, **options)

    def tear_down_driver(self, interface):
        super().tear_down_driver(interface)
        interface.quit()

    def capture(self, interface, config):
        super().capture(interface, config)

        interface.visit(config["url"])
        screenshot_path = interface.screenshot(config["destination"],
                                               full=True)

        return screenshot_path


class SplinterChromeScreenshot(SplinterFirefoxScreenshot):
    """
    Using Chrome browser through Splinter.
    """
    DESTINATION_FILEPATH = "{name}_chrome_splinter.png"
    BROWSER_TYPE = "chrome"
