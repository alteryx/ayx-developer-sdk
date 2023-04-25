# DCM Input Example Tool
:::

::: node--info
::: node--info--modified
Last modified: February 16, 2022
:::
:::

::: {.paragraph .paragraph--type--simple-content .paragraph--view-mode--default}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
## Overview {#overview .index-item}

The [Data Connection Manager (DCM)
feature](../20223/designer/dcm-designer.html "Data Connection Manager (DCM)"){entity-substitution="canonical"
entity-type="node" entity-uuid="73de3bee-6a9e-477f-a978-13f249edc18f"
rel="noopener" target="_blank"} provides the ability to securely create,
retrieve, update, delete, and synchronize Data Sources, Credentials, and
Connections (Credentials linked to a Data Source). Only a small subset
of these functions is accessible from the Python SDK.

The DCM Input tool example demonstrates how to use all these functions.

## DCM Configuration {#dcm-configuration .index-item}

The DCM Input tool requires the DCM feature to be enabled in Alteryx
Designer. You can do this via the Admin configuration:

1.  Navigate to **Options** \> **Advanced Options** \> **System
    Settings**.
2.  Navigate to the **DCM** \> **General** section and select the
    **Enable DCM for your Organization** check box.

You can also enable DCM via Designer's User Settings:

1.  In Designer, navigate to **Options** \> **User Settings** \> **Edit
    User Settings**.
2.  Open the **DCM** tab.
3.  Select **Override DCM Settings** and select **Enable DCM**.

Please go to the [DCM
Documentation](../20223/designer/dcm-designer.html "DCM Documentation"){entity-substitution="canonical"
entity-type="node" entity-uuid="73de3bee-6a9e-477f-a978-13f249edc18f"
rel="noopener" target="_blank"} for more information about DCM
configuration.

## Prepare the DCM Connection {#prepare-the-dcm-connection .index-item}

The DCM Input tool requires the DCM connection ID to work. To create a
DCM connection, in Designer...

1.  Navigate to **File** \> **Manage Connections**.
2.  By default, the **Manage Connections** window shows a list of
    available Data Sources.
3.  Select **Credentials** to check the available Credentials.
4.  Use the **Add Credential** button to create a new credential, if
    needed.
5.  Return to the **Data Sources** tab and select the desired Data
    Source from the list.
6.  Select **Connect Credential** to create a new DCM connection.
7.  Specify your desired **Authentication Method** and select a
    credential from the list.
8.  Make sure to check the box to **Allow connection for SDK** or this
    connection will not be accessible from the Python SDK.
9.  Select the **Link** button to finalize the creation of the
    connection.

## Use the Tool {#use-the-tool .index-item}

If you know the DCM connection ID, select the DCM Input tool and enter
DCM connection ID in the DCM ID field.

If you don\'t know the connection ID...

1.  Select the DCM Input tool and select the **Set DCM ID from
    Connection Manager...** button.
2.  Select your desired Data Source and it will display the available
    connections.
3.  Select the **Connect** button for the connection that you want to
    use.
4.  Use the **Enter new password** field to specify a new password for
    this connection.
5.  Once your workflow runs, the DCM Input tool gets connection
    information, acquires a write-lock for it, updates the connection
    with a new password, and frees the write-lock.

## Python SDK DCM API {#python-sdk-dcm-api .index-item}

A special \"dcm\" Provider of the PluginV2 class contains these
asynchronous methods to work with DCM:

#### 5.1 get_connection()

`get_connection( conection_id: str, callback_fn: Callable)`

This method retrieves connection information (including secrets) by
connection ID and passes it to `callback_fn` function as a dictionary.

-   Input parameters:
    -   connection_id: A connection ID.
    -   callback_fn: A callback function that is executed once the DCM
        request is executed.
-   Output to the callback:
    -   Dict that contains connection information for the specified ID,
        including secret values.

#### 5.2 get_write_lock()

`get_write_lock( connection_id: str, role: str, secret_type: str, expires_in: Optional["dt.datetime"], callback_fn: Callable)`

This method attempts to acquire an exclusive write lock.

-   Input parameters:
    -   connection_id: A connection ID.
    -   role: A role connection parameter.
    -   secret_type: A secret type connection parameter.
    -   expires_in: (Optional) A value that asks how long the lock
        should be held for (in milliseconds).
    -   callback_fn: A callback function that is executed once the DCM
        request is executed.
-   Output to the callback:
    -   Dict that contains an `expires_in` value and a `lock_id`*.*

#### 5.3 free_write_lock()

`free_write_lock(connection_id: str, role: str,secret_type: str,lock_id: str,callback_fn: Optional[Callable])`

This method frees a lock obtained from a previous call to
`get_write_lock()`.

-   Input parameters:
    -   connection_id: A connection ID.
    -   role: A role connection parameter.
    -   secret_type: A secret type connection parameter.
    -   lock_id: Lock ID acquired from a previous call to
        `get_write_lock()`*.*
    -   callback_fn: A callback function that is executed once the DCM
        request is executed.
-   Output to the callback:
    -   N/A. Exception raised upon failure.

#### update_connection_secret()

`update_connection_secret(connection_id: str, role: str, secret_type: str, value: str, expires_on: Optional["dt.datetime"], parameters: Optional[Dict[str, str]], lock_id: str, callback_fn: Optional[Callable])`

This method updates a single secret for *role* and *secret_type* to
*value* as well as the optional `expires_on` and `parameters`.

-   Input parameters:
    -   connection_id: A connection ID.
    -   role: A role connection parameter.
    -   secret_type: A secret type connection parameter.
    -   lock_id: Lock ID acquired from a call to `get_write_lock()`*.*
    -   value: The new value to store for the secret.
    -   expires_on: (Optional) Expiration of this secret.
    -   parameters: (Optional) Dict of parameter values for this secret.
        This is arbitrary user data stored as JSON.
-   Output to the callback:
    -   N/A. Exception raised upon failure.