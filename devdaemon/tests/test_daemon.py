"""Tests for the core daemon classes."""

from twisted.trial import unittest
from devdaemon.daemon import DevDaemonService
from mock import Mock


class DaemonServiceTest(unittest.TestCase):

    """Some tests for the DaemonService class."""

    def setUp(self):  # noqa
        options = {}
        self.daemon = DevDaemonService(options)

    def test_init(self):
        """Test we can make a daemon service."""
        self.assertTrue(self.daemon)

    def test_start_work(self):
        """Test starting some work."""
        self.daemon.timer = Mock()
        self.daemon.issues = Mock()
        self.daemon.start_work(1)

    def test_stop_work(self):
        """Test stopping some work."""
        self.daemon.timer = Mock()
        self.daemon.stop_work()
