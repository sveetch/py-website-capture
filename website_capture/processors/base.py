class ProcessorBase(object):
    """
    Basic processor don't do anything except exposing required methods
    signatures.

    Attributes:
        name (string): Processor name used to store its report datas or
            logging possible events. Each processor must have an unique name.
    """
    name = "basic"

    def __init__(self, *args, **kwargs):
        pass

    def run(self, driver, config, response):
        """
        This is where your processor should perform its work and possibly
        returns datas to append to processor reports which will be stored with
        processor name.
        """
        return None
