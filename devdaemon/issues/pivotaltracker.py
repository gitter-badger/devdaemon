"""Pivotal tracker issue management."""

from twisted.internet import defer
from twisted.python import log
import treq
import json


class PivotalTrackerIssues(object):

    """Pivotal tracker issues management."""

    def __init__(self, options):
        """Set up API basics."""
        self._options = options
        self.token = "e8d2ec75253d7f30dba16d3e463448aa"
        self.project_id = "1120728"
        self.api_base =\
            "https://www.pivotaltracker.com/services/v5/projects/{}/"\
            .format(self.project_id)

    def treq_get(self, url):
        """Wrap get request to api."""
        return treq.get(
            url, headers={"X-TrackerToken": self.token}
        ).addCallback(lambda resp: resp.json())

    def treq_send(self, method, url, data):
        """Wrap send put/post to api."""
        json_data = json.dumps(data)
        return getattr(treq, method)(url, json_data, headers={
            "X-TrackerToken": self.token,
            "Content-Type": "application/json"
        }).addCallback(lambda resp: resp.json())

    def get_comment(self, issue_id, comment_id):
        """Get a comment from PT."""
        url = self.api_base + "stories/{}/comments/{}"\
            .format(issue_id, comment_id)
        return self.treq_get(url)

    def create_comment(self, issue_id, notes):
        """Create a comment on PT."""
        url = self.api_base + "stories/{}/comments".format(issue_id)
        return self.treq_send("post", url, {"text": notes}).addCallback(
            self.handle_response)

    def handle_response(self, data):
        """Some data."""
        return data['id']

    @defer.inlineCallbacks
    def finish_comment(self, issue_id, comment_id, notes):
        """Finish up the comment on PT."""
        log.msg("Sending finish comment: issue: {}, comment: {}".format(
            issue_id, comment_id))

        comment = yield self.get_comment(issue_id, comment_id)
        text = comment['text']
        text += "\n\n" + notes
        url = self.api_base + "stories/{}/comments/{}"\
            .format(issue_id, comment_id)
        response = yield self.treq_send("put", url, {"text": text})
        defer.returnValue(self.handle_response(response))

    def set_issue_started(self, issue_id):
        """Set the issue as started."""
        url = self.api_base + "stories/{}"\
            .format(issue_id)
        data = {"current_state": "started"}
        return self.treq_send("put", url, data).addCallback(
            self.handle_response)
