import logging


class LogProvider(object):
    """
    Logger provider
    """
    def __init__(self, log_file_name, log_level):
        self.log_file_name = log_file_name
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.propagate = False
        self.fh = logging.FileHandler(log_file_name, "w")
        self.fh.setLevel(log_level)
        self.logger.addHandler(self.fh)
        self.keep_fds = [self.fh.stream.fileno()]

    def get_logger(self):
        return self.logger

    def get_fds(self):
        return self.keep_fds


