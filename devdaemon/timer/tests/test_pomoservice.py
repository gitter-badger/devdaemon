"""Tests for the pomodoro service."""

from twisted.trial import unittest
from twisted.internet import task
from devdaemon.timer.pomodoro import PomoTimer


class PomodoroTimerTest(unittest.TestCase):

    def setUp(self):  # noqa
        self.pomo = PomoTimer()
        self.pomo.reactor = task.Clock()

    def test_init(self):
        """Test we can make one."""
        self.assertTrue(self.pomo)

    def test_start_finish(self):
        """Test starting it."""
        d = self.pomo.start()
        d.addCallback(self._on_done, None)
        self.pomo.reactor.advance(self.pomo.duration * 60)
        return d

    def _on_done(self, res, assert_result):
        self.assertEqual(res, assert_result)

    def test_start_cancel(self):
        """Test starting then manually cancelling."""
        d = self.pomo.start()
        d.addCallback(self._on_done, "Cancelled.")
        d.cancel()
        return d

    def test_start_stop(self):
        """Test starting then stopping."""
        d = self.pomo.start()
        d.addCallback(self._on_done, "Stopped.")
        self.pomo.stop("Stopped.")
        return d

    def test_start_pause(self):
        d = self.pomo.start()
        self.pomo.pause()
        self.pomo.unpause()
        self.pomo.reactor.advance(self.pomo.duration * 60)
        return d
