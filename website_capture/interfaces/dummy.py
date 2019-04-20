from website_capture.interfaces.base import BaseScreenshot


class DummyInterface(object):
    """
    Fake interface for dummy test usage
    """
    def visit(self, url):
        return f"Pretend to visit url: {url}"

    def get(self, url):
        return f"Pretend to get url: {url}"

    def find_element_by_tag_name(self, name):
        return self

    def screenshot(self, path, **kwargs):
        return path


class DummyScreenshot(BaseScreenshot):
    """
    Does not implement a real interface it just perform tasks and print out
    some debugging information.
    """
    INTERFACE_CLASS = DummyInterface

    def get_interface_instance(self, config):
        klass = self.get_interface_class()
        return klass()

    def capture(self, interface, size, page):
        path = super().capture(interface, size, page)
        return path
