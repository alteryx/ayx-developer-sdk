Tool Configurations
===================

When you create new Ayx Plugin tools through the Core SDK CLI, tool
configurations place new tools in the `Python SDK Examples` category in
Alteryx Designer. You likely don\'t want your new tools to live within
that category. In order to modify Designer\'s interactions with your
tools, you must change the tool configuration XML file. Within an Ayx
Plugin Tool directory, you can view and modify these settings in the
`{tool_name}Config.xml` file.

These are the permissible XML tags and their explanations:

> -   `<AlteryxJavaScriptPlugin>`: Wrapper around Alteryx Plugins built
>     in HTML and JavaScript.
> -   `<EngineSettings>`: Settings that indicate how to run the
>     underlying tool engine (in this case written in Python).
>
>     > -   `EngineDll`: The type of engine to use, in other words,
>     >     Python.
>     > -   `EngineDllEntryPoint`: The entry point file to the Python
>     >     engine. In the case of the example tools, they point to
>     >     main.py. Any Python file can be the entry point as long as
>     >     it implements the core plugin and registers itself.
>     > -   `SDKVersion`: The version of the Alteryx Python SDK. Current
>     >     version is 10.1.
>     > -   `ToolFamily`: The Tool Family this plugin belongs to.
>
> -   `<GuiSettings>`: The settings for the Configuration panel GUI.
>
>     > -   `Html`: The HTML file to render in the Configuration panel.
>     > -   `Icon`: Points to the icon file to use for the Ayx Plugin
>     >     Tool in Alteryx Designer.
>     > -   `SDKVersion`: The version of the UI SDK. Current version is
>     >     10.1.
>
> -   `<InputConnections>`: The input anchors for the Ayx Plugin Tool.
>
>     > -   `<Connection>`: An individual anchor attached to the tool.
>     > -   `Name`: The name of the input anchor. This name is
>     >     referenced in the Alteryx Core SDK to look up anchors for
>     >     receiving and setting data.
>     > -   `AllowMultiple`: A flag that indicates whether multiple
>     >     connections can be fed into this anchor.
>     > -   `Optional`: A flag that indicates whether a connection to
>     >     and from this anchor is required for the Ayx Plugin Tool to
>     >     run.
>     > -   `Type`: Indicates the type of anchor. This should always be
>     >     a `Connection` type.
>     > -   `Label`: A 1-character label placed on the anchor when the
>     >     tool is placed in Alteryx Designer.
>
> -   `<OutputConnections>`: Output anchors for the Ayx Plugin Tool.
> -   `<Properties>`: Properties of the Ayx Plugin Tool used by Alteryx
>     Designer.
> -   `<MetaInfo>`: General information about the Ayx Plugin Tool used
>     by Alteryx Designer.
> -   `<Name>`: The name of the tool as it should appear in Alteryx
>     Designer.
> -   `<Description>`: The description that appears when the tool is
>     selected in Alteryx Designer.
> -   `<ToolVersion>`: The version of the Ayx Plugin Tool. This version
>     is managed by the developer but also consumed by Alteryx Designer.
> -   `<CategoryName>`: Indicates to Alteryx Designer what tool category
>     to use, for example, `SDK Examples`.
> -   `<SearchTags>`: A comma-separated list of descriptive words used
>     in the search bar in Alteryx Designer.
> -   `<Author>`: That\'s you!
> -   `<Company>`: The name of the company (can be left blank).
> -   `<Copyright>`: The year of tool copyright.

**Takeaways**

-   The `<EngineSettings>` and `<GuiSettings>` are used by both Alteryx
    Designer and the Alteryx Core SDK to generate the anchors and
    connections necessary to feed in and push out data from your Ayx
    Plugin Tool when Designer executes the tool\'s engine via the
    **Run** command.
-   The `<Properties>` are used *only* by Alteryx Designer for the
    aesthetics of the tool.
