from website_capture.interfaces.base import BaseInterface


class DummyDriver(object):
    """
    Fake driver for dummy test usage
    """
    def visit(self, url):
        return f"Pretend to visit url: {url}"

    def get(self, url):
        return f"Pretend to get url: {url}"

    def find_element_by_tag_name(self, name):
        return self

    def screenshot(self, path, **kwargs):
        return path


class DummyInterface(BaseInterface):
    """
    Does not implement a real interface with a working driver. It just perform
    tasks and print out some debugging information. Mainly for dev and tests
    usage.
    """
    DRIVER_CLASS = DummyDriver

    def get_driver_instance(self, options, config):
        klass = self.get_driver_class()
        return klass()
