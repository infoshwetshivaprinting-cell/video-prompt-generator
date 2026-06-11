import unittest
import os
from logger import log_info, log_error, LOG_FILE

class TestLogger(unittest.TestCase):

    def setUp(self):
        """Ensure log file starts fresh for each test."""
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

    def test_log_info(self):
        """Test if log_info writes the correct entry."""
        log_info("This is a test info log.")
        with open(LOG_FILE, "r") as log:
            content = log.read()
        self.assertIn("This is a test info log.", content)

    def test_log_error(self):
        """Test if log_error writes the correct entry."""
        log_error("This is a test error log.")
        with open(LOG_FILE, "r") as log:
            content = log.read()
        self.assertIn("This is a test error log.", content)

if __name__ == "__main__":
    unittest.main()