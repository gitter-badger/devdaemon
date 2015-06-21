"""The core service that ties everything together."""

from zope.interface import implements
from twisted.application.service import Service, MultiService
from twisted.internet import task, defer, reactor  # noqa
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.python import usage
from twisted.application import strports
from twisted.python import log
from os.path import expanduser

from devdaemon.timer.pomodoro import PomoTimer
from devdaemon.issues.pivotaltracker import PivotalTrackerIssues
from devdaemon.ui.alerts import ZenityAlerts

from txjsonrpc.netstring import jsonrpc


class DevDaemonService(Service):

    """The DevDaemon service pulls everything together."""

    def __init__(self, options):  # noqa
        self._options = options
        self.timer = self.make_timer()
        self.issues = self.make_issues()
        self.alerts = self.make_alerts()
        self._on_timer_finished = None
        self.comment_id = None
        self.issue_id = None

    def start_work(self, issue_id, notes=""):
        """Start working on a task."""
        notes = "POMO duration:{}m\n".format(self.timer.duration) + notes
        self._on_timer_finished = self.timer.start()
        self._on_timer_finished.addCallback(self._timer_finished)
        self.issues.set_issue_started(issue_id)
        d = self.issues.create_comment(issue_id, notes)
        d.addCallback(self._comment_sent, issue_id)
        return d

    def stop_work(self, reason=None):
        """Stop working on a task."""
        self.timer.stop(reason)
        return True

    def _timer_finished(self, result):
        log.msg("Timer finished up: {}".format(result))
        notes = "POMO done."
        if not result:
            self.alerts.info("Pomodoro done!")
            return self.issues.finish_comment(
                self.issue_id, self.comment_id, notes)
        else:
            log.msg("Woopsie.. stopped the timer.")

    def _comment_sent(self, result, issue_id):
        self.issue_id = issue_id
        self.comment_id = result
        return True

    def make_timer(self):
        """Eventually allow dynamic choosing of timer."""
        return PomoTimer(self._options)

    def make_issues(self):
        """Eventually allow dynamic issue tracking choice."""
        return PivotalTrackerIssues(self._options)

    def make_alerts(self):
        """Eventually make pluggable."""
        return ZenityAlerts()


class DevDaemonJSONRPC(jsonrpc.JSONRPC, object):

    """JSON RPC for dev daemon."""

    def __init__(self, *args, **kwargs):
        """Set up rpc to wrap daemon service."""
        self.devdaemon = kwargs.pop("devdaemon")
        super(DevDaemonJSONRPC, self).__init__(*args, **kwargs)

    def jsonrpc_start(self, issue_id, message=None):
        """Wrap starting a body of work."""
        return self.devdaemon.start_work(issue_id, message)

    def jsonrpc_stop(self, message=None):
        """Wrap stopping."""
        return self.devdaemon.stop_work(message)


class Options(usage.Options):

    """Options for the service."""


class DevDaemonServiceMaker(object):

    """Service maker for the daemon."""

    implements(IServiceMaker, IPlugin)
    tapname = "devdaemon"
    description = "The DevDaemon service."
    options = Options

    def makeService(self, options):
        """Create the collection of services."""
        service = MultiService()
        devdaemon = DevDaemonService(options)
        devdaemon.setServiceParent(service)
        factory = jsonrpc.RPCFactory(DevDaemonJSONRPC(devdaemon=devdaemon))
        rpc = strports.service(
            "unix:address={}/.devdaemon.sock".format(expanduser("~")),
            factory=factory
        )
        rpc.setServiceParent(service)
        return service
