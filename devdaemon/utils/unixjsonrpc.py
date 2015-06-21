"""Some utils to do jsonrpc over unix sockets."""
from twisted.internet import reactor
from txjsonrpc.jsonrpc import BaseProxy
from txjsonrpc.netstring.jsonrpc import QueryFactory, QueryProtocol
from twisted.internet.endpoints import clientFromString
from txjsonrpc import jsonrpclib


class UnixQueryProtocol(QueryProtocol):

    """Dont depend on the socket disconnecting."""

    def stringReceived(self, string):
        """Got a string response."""
        self.factory.data = string
        self.factory.parseResponse(string)


class UnixQueryFactory(QueryFactory):

    protocol = UnixQueryProtocol


class UnixProxy(BaseProxy):

    """
    A Proxy for making local JSON-RPC calls.

    Pass the filenameof the JSON-RPC server socket to the constructor.

    Use proxy.callRemote('foobar', *args) to call remote method
    'foobar' with *args.
    """

    def __init__(self, path, version=jsonrpclib.VERSION_PRE1,
                 factoryClass=UnixQueryFactory):
        """
        @type host: C{str}
        @param host: The host to which method calls are made.

        @type port: C{integer}
        @param port: The host's port to which method calls are made.

        @type version: C{int}
        @param version: The version indicates which JSON-RPC spec to support.
        The available choices are jsonrpclib.VERSION*. The default is to use
        the version of the spec that txJSON-RPC was originally released with,
        pre-Version 1.0.

        @type factoryClass: C{object}
        @param factoryClass: The factoryClass should be a subclass of
        QueryFactory (class, not instance) that will be used instead of
        QueryFactory.
        """
        BaseProxy.__init__(self, version, factoryClass)
        self.path = path

    def callRemote(self, method, *args, **kwargs):
        version = self._getVersion(kwargs)
        factoryClass = self._getFactoryClass(kwargs)
        factory = factoryClass(method, version, *args)
        endpoint = clientFromString(
            reactor, self.path)
        endpoint.connect(factory)
        return factory.deferred
