from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from website_capture.interfaces.base import BaseScreenshot

from website_capture.settings import *

class SeleniumFirefoxScreenshot(BaseScreenshot):
    """
    Using Firefox browser directly from WebDriver through Selenium.

    Here the interface is a browser driver.
    """
    DESTINATION_FILEPATH = "{name}_firefox_selenium.png"
    INTERFACE_CLASS = webdriver.Firefox

    def get_interface_instance(self, options):
        klass = self.get_interface_class()
        interface = klass(options=options)

        return interface

    def set_interface_size(self, interface, size):
        interface.set_window_size(*size)

    def get_interface_config(self):
        options = FirefoxOptions()

        if self.headless:
            options.headless = True

        return options

    def capture(self, interface, size, page):
        path = super().capture(interface, size, page)

        interface.get(page["url"])

        el = interface.find_element_by_tag_name('body')
        el.screenshot(path)

        return path

    def tear_down_runner(self, interface, size, pages):
        super().tear_down_runner(interface, size, pages)
        interface.quit()


class SeleniumChromeScreenshot(SeleniumFirefoxScreenshot):
    """
    Using Chrome browser directly from WebDriver through Selenium.
    """
    DESTINATION_FILEPATH = "{name}_chrome_selenium.png"
    INTERFACE_CLASS = webdriver.Chrome

    def get_interface_config(self):
        options = ChromeOptions()
        if self.headless:
            options.headless = True

        return options

    def capture(self, interface, size, page):
        path = super().capture(interface, size, page)

        interface.get(page["url"])

        interface.get_screenshot_as_file(path)

        return path


if __name__ == "__main__":
    print("🤖 SeleniumFirefoxScreenshot")
    print()
    screenshoter = SeleniumFirefoxScreenshot(
        basedir=DUMPS_PATH,
    )
    screenshoter.run(pages=PAGES)
    print()

    print("🤖 SeleniumChromeScreenshot")
    print()
    screenshoter = SeleniumChromeScreenshot(
        basedir=DUMPS_PATH,
    )
    screenshoter.run(pages=PAGES)
    print()
