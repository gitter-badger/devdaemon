"""A service to run a pomodoro timer."""
from datetime import datetime
from .workblock import WorkBlock
from twisted.internet import task, defer, reactor
from twisted.python import log


class Pomodoro(WorkBlock):

    """Wrap a block of work with pomo stuff."""


class PomoTimer(object):

    """A pomodoro timer."""

    reactor = reactor

    def __init__(self, options=None):  # noqa
        self._options = options or {}
        self.duration = self._options.get("POMO_DURATION", 30)
        self.idle_duration = self._options.get("POMO_IDLE_DURATION", 5)
        self.current_deferred = None
        self.started_at = None
        self.paused_elapsed = None
        self.paused_at = None
        self.unpaused_at = None
        self.on_finished = defer.Deferred(self.cancel)

    def start(self):
        """Start a pomodoro."""
        log.msg("Starting timer.")
        if self.current_deferred:
            raise ValueError("We are already started.")
        self.reset()
        self.current_deferred = task.deferLater(
            self.reactor,
            self.duration * 60,
            self.finish
        ).addErrback(self._on_err)
        self.started_at = datetime.now()
        return self.on_finished

    def stop(self, reason):
        """Stop a pomodoro."""
        log.msg("Stopping a timer.")
        return self.finish(reason)

    def cancel(self, deferred):
        """Cancel it."""
        deferred.callback("Cancelled.")
        self.current_deferred, d = None, self.current_deferred
        d.cancel()

    def pause(self):
        """Pause a pomodoro."""
        log.msg("Paused.")
        self.paused_at = datetime.now()
        self.paused_elapsed = self.get_elapsed()
        self.current_deferred, d = None, self.current_deferred
        d.cancel()

    def unpause(self):
        """Unpause a pomodoro."""
        log.msg("Unpaused.")
        self.unpaused_at = datetime.now()
        self.current_deferred = task.deferLater(
            self.reactor,
            (self.duration * 60) - self.paused_elapsed.total_seconds(),
            self.finish
        ).addErrback(self._on_err)

    def _on_err(self, error):
        log.err("Some error happened.")
        error.trap(defer.CancelledError)
        self.current_deferred = None

    def finish(self, reason=None):
        """Finish a pomodoro."""
        log.msg("Finishing up now, reason: {}".format(reason))
        self.current_deferred, d = None, self.current_deferred
        d.cancel()
        d, self.on_finished = self.on_finished, defer.Deferred(self.cancel)
        d.callback(reason)

    def get_elapsed(self):
        """Get the elapsed time for this pomo."""
        elapsed = datetime.now() - self.started_at
        return elapsed

    def reset(self):
        """Reset the pomo."""
        self.started_at = None
        self.paused_elapsed = None
        self.paused_at = None
        self.unpaused_at = None
        self.current_deferred = None
