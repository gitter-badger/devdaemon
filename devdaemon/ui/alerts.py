"""Do alerts some how."""

from twisted.internet.utils import getProcessValue
import os


class ZenityAlerts(object):

    """
    Manage alerts.

    https://help.gnome.org/users/zenity/stable/message.html.sv

    We're using a combo of CLI and zenity by default.
    """

    def run(self, type, text):
        d = getProcessValue(
            "zenity",
            args=(type, "--text", text),
            env=os.environ
        )
        return d

    def info(self, text):
        """Alert some information."""
        return self.run("--info", text)


    def question(self, text):
        """Alert with a question."""
