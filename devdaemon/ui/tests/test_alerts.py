"""Tests for alerts."""

from twisted.trial import unittest
from twisted.internet import defer
from devdaemon.ui.alerts import ZenityAlerts
from mock import Mock, patch


class DefaultTest(unittest.TestCase):

    """Test for the alerts."""

    def setUp(self):  # noqa
        self.alert = ZenityAlerts()
        self.alert.run = Mock()
        self.alert.run.return_value = defer.succeed(None)

    def test_info(self):
        """Test showing info."""
        d = self.alert.info("Hi there.")
        d.addCallback(
            lambda ign:
            self.alert.run.assert_called_with("--info", "Hi there."))
        return d


class AlertRunTest(unittest.TestCase):

    """Separate test for the run method."""

    @patch("devdaemon.ui.alerts.getProcessValue")
    def test_run(self, gpv):
        """Test running."""
        alert = ZenityAlerts()
        alert.run("foo", "bar")
        self.assertEqual(1, gpv.call_count)
