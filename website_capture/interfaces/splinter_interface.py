from splinter import Browser

from website_capture.interfaces.base import BaseScreenshot


class SplinterFirefoxScreenshot(BaseScreenshot):
    """
    Using Firefox browser through Splinter interface which is a layer on top
    of WebDriver through Selenium.

    Here the interface is the Splinter "browser" object.
    """
    DESTINATION_FILEPATH = "{name}_firefox_splinter.png"
    BROWSER_TYPE = "firefox"

    def set_interface_size(self, interface, config):
        interface.driver.set_window_size(*config["size"])

    def get_interface_options(self, config):
        options = {}

        if self.headless:
            options["headless"] = True

        options["log_path"] = config["log_path"]

        return options

    def get_interface_instance(self, options):
        return Browser(self.BROWSER_TYPE, **options)

    def capture(self, interface, config):
        super().capture(interface, config)

        interface.visit(config["url"])
        screenshot_path = interface.screenshot(config["destination"],
                                               full=True)

        return screenshot_path

    def tear_down_interface(self, interface):
        super().tear_down_interface(interface)
        interface.quit()


class SplinterChromeScreenshot(SplinterFirefoxScreenshot):
    """
    Using Chrome browser through Splinter.
    """
    DESTINATION_FILEPATH = "{name}_chrome_splinter.png"
    BROWSER_TYPE = "chrome"
