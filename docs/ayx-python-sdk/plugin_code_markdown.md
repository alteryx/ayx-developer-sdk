Plugin Tool Execution Framework
===============================

Plugin Class
------------

The Plugin class is the basis for all Ayx Plugin Tools in the new Core
SDK. The abstract Plugin class provides the required abstract methods
that need to be implemented in order for a tool to interact with Alteryx
Designer. These interactions are mediated by the Providers, which
provide simplified interfaces for Designer functionality and drive the
execution of the Ayx Plugin Tools. For more information on the execution
flow, see [Plugin
Lifecycle](https://extensibility.pages.git.alteryx.com/ayx-sdks/plugin_lifecycle.html).

Register the Plugin
-------------------

Every plugin must be registered with the Core SDK after the new Ayx
Plugin Tool class is defined. The Ayx Plugin Tool must implement the
base Plugin class in order for the Core SDK to accept the registered
plugin. The registration process indicates to the Core SDK that the
Plugin exists, what the name of the class is, and provides a means of
driving the Ayx Plugin Tool\'s execution.

The init Method
---------------

The `__init__` method in the Ayx Plugin Tool class initializes relevant
properties. It is also the access point for the BaseProvider object to
all of the Plugin methods, so the provider is typically stored as a
class variable in the init method. The init is also the point when
anchors are set from the provider.

The on\_incoming\_connection\_complete Method
\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~

The `on_incoming_connection_complete` method is called to handle any
additional work for a completed anchor. The method is called when there
are no more records left. It notifies the plugin that the connection is
done sending data.

This method receives an `Anchor` object that contains the anchor name
(`anchor.name`) and the corresponding input connection
(`anchor.connection`).

The on\_record\_batch Method
----------------------------

The `on_record_batch` method is called for each input connection on an
anchor.

This method also receives an `Anchor` object (as well as all the records
and data sent from E2) in the form of a [PyArrows
Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html).

In this method, the plugin writer can manipulate the data before writing
the data to the output anchor using
`self.provider.write_to_anchor(self.output_anchor_name, table)`

The on\_complete Method
-----------------------

The `on_complete` method is called at the end of the runtime execution.

This typically does any cleanup required for the Ayx Plugin Tool. If the
plugin is an Input tool-type, this method is used to read in the data
from the datasource and push it to the output anchor. (since an Input
tool-type has no input anchors or connections, and therefore
`on_incoming_connection_complete` and `on_record_batch` are not called).

Proxy Environment Configuration
-------------------------------

If you are running your plugin on a network that requires a proxy, you
might encounter errors when you make external requests (An API as a data
source, for example) We provide a convience function to inherit
configuration from Designer in `proxy_requests`. The
`proxy_requests.create_proxied_session` function returns a `PACSession`
initialized with any found Designer proxy authentication settings. If
you need any addition configuration, you can extend the `PACSession`
further; see the [PyPAC Docs](https://pypac.readthedocs.io/en/latest/)
for more info.
