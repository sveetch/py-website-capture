from splinter import Browser

from website_capture.interfaces.base import BaseScreenshot

from website_capture.settings import *

class SplinterFirefoxScreenshot(BaseScreenshot):
    """
    Using Firefox browser through Splinter interface which is a layer on top
    of WebDriver through Selenium.

    Here the interface is the Splinter "browser" object.
    """
    DESTINATION_FILEPATH = "{name}_firefox_splinter.png"
    BROWSER_TYPE = "firefox"

    def get_interface_config(self):
        options = {}

        if self.headless:
            options["headless"] = True

        return options

    def set_interface_size(self, interface, size):
        interface.driver.set_window_size(*size)

    def get_interface_instance(self, options):
        return Browser(self.BROWSER_TYPE, **options)

    def capture(self, interface, size, page):
        path = super().capture(interface, size, page)

        interface.visit(page["url"])
        screenshot_path = interface.screenshot(path, full=True)

        return screenshot_path

    def tear_down_runner(self, interface, size, pages):
        super().tear_down_runner(interface, size, pages)
        interface.quit()


class SplinterChromeScreenshot(SplinterFirefoxScreenshot):
    """
    Using Chrome browser through Splinter.
    """
    DESTINATION_FILEPATH = "{name}_chrome_splinter.png"
    BROWSER_TYPE = "chrome"


if __name__ == "__main__":
    print("🤖 SplinterFirefoxScreenshot")
    print()
    screenshoter = SplinterFirefoxScreenshot(
        basedir=DUMPS_PATH,
    )
    screenshoter.run(pages=PAGES)
    print()

    print("🤖 SplinterChromeScreenshot")
    print()
    screenshoter = SplinterChromeScreenshot(
        basedir=DUMPS_PATH,
    )
    screenshoter.run(pages=PAGES)
    print()
