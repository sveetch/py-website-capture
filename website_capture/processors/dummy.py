from .base import ProcessorBase


class DummyProcessor(ProcessorBase):
    """
    A dummy processor for test purpose.
    """
    name = "dummy"

    def run(self, driver, config, response):
        return "Dummy report"
