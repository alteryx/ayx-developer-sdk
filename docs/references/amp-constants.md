# AMP Constants

AMP Constants are the information passed from the AMP Engine to the tool.

## Constants
Here is a list of constants passed from the engine to the tool:
- **_designer_version**: The current version of Designer.
- **_alteryx_install_dir**: The path to the installation directory of the Designer executable.
- **_workflow_dir**: The path to the directory the current workflow is in.
- **_temp_dir**: The path to the temp directory where runtime data is stored.
- **_tool_id**: The ID of the tool.
- **_workflow_id**: The ID of the current workflow.
- **_raw_constants**: The rest of the data sent by the engine in its raw format:
    - **AdditionalAliasFile**
    - **AlteryxExecutable**: The path to the Designer executable.
    - **CallerProductId**: The ID of the caller.
    - **ConvErrorLimit**: The amount of conversion errors the engine can encounter before stopping.
    - **DefaultDir**: The default directory for Designer.
    - **DefaultTempDir**: The default directory for Designer to write temp files to.
    - **DisableAllOutput**: Indicates whether output from Designer has been disabled.
    - **DisableBrowse**: Indicates whether browse everywhere has been disabled.
    - **EnablePerformanceProfiling**: Indicates whether performance profiling has been enabled.
    - **Engine.GuiInteraction**: Indicates whether the workflow is being run from the GUI.
    - **Engine.IterationNumber**: The number of times a macro has run.
    - **Engine.ModuleDirectory**: The location where the engine module is located.
    - **Engine.OS**: The OS Designer is running on.
    - **Engine.ReportFont**: The font the engine reports are written in.
    - **Engine.TempFilePath**: The path where the engine writes temp files.
    - **Engine.Type**: The type of engine designer runs on.
    - **Engine.Version**: The version of the engine Designer uses.
    - **Engine.WorkflowDirectory**: The directory of the current workflow.
    - **Engine.WorkflowFileName**: The file name of the workflow (this is only available if the workflow has been saved).
    - **GlobalRecordLimit**: The maximum amount of records Designer can process.
    - **JupyterTempPath**: The temp path Jupyter writes to.
    - **ModuleDirectory**: The directory Designer module is stored in.
    - **OutputConnectionMetaDataMessages**: Indicates whether output connection metadata messages are enabled.
    - **PredictiveCodePage** 
    - **ProxyConfiguration**: Used to proxy network requests.
    - **RestrictedDataMode**
    - **RunMode**: Indicates how the engine interacts with Designer.
    - **SerialNumber**: The serial number for Designer.
    - **SortedGrouping** 
    - **TempPath**: The path where Designer writes temp files.
    - **ToolId**: The ID of the current tool.
    - **UpdateOnly** 
    - **UseVfs**
    - **WorkflowDirectory**: The directory of the current workflow.
    - **WorkflowRunGuid**: The GUID of the current workflow run.

## Usage
To access the constants, run this command:

    def __init__(self, provider)
        desired_constant = self.provider.environment.*constant*

To access the constants stored in the **_raw_constants**, run this command:
    
    def __init__(self, provider)
        desired_constant = self.provider.environment._raw_constants[*constant*]