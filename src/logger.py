import logging

LOG_LEVEL = logging.DEBUG

class PrawLogger:

    def __init__(self):
      self.log = logging.getLogger("Praw")
      self.log.setLevel(LOG_LEVEL)

      # System out stream handler
      sys_out_handler = logging.StreamHandler()
      sys_out_handler.setLevel(LOG_LEVEL)

      # System out stream formatting
      sys_out_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
      sys_out_handler.setFormatter(sys_out_formatter)

      self.log.addHandler(sys_out_handler)

    def error_log(self, error):
      self.log.error(str(error), exc_info=True)
