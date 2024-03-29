# AMP Constants

Amp Constants are the information passed from the AMP Engine to the tool

## Constants
Here is a list of constants passed from the engine to the tool:
- **_designer_version** the current version of designer
- **_alteryx_install_dir** the path to the installation directory of the designer executable
- **_workflow_dir** the path to the directory the current workflow is in
- **_temp_dir** the path to the temp directory where runtime data is stored
- **_tool_id** the id of the tool
- **_workflow_id** the id of the current workflow
- **_raw_constants** the rest of the data sent by the engine in its raw format:
    - **AdditionalAliasFile**
    - **AlteryxExecutable** path to the designer executable
    - **CallerProductId** the ID of the caller
    - **ConvErrorLimit** the amount of conversion errors the engine can encounter before stopping
    - **DefaultDir** the default directory for designer
    - **DefaultTempDir** the default directory for designer to write temp files to
    - **DisableAllOutput** if output from designer has been disabled
    - **DisableBrowse** if browse everywhere has been disabled
    - **EnablePerformanceProfiling** if performance profiling has been enabled
    - **Engine.GuiInteraction** if the workflow is being run form the GUI
    - **Engine.IterationNumber** the number of times a macro has run
    - **Engine.ModuleDirectory** where the engine module is located
    - **Engine.OS** the OS designer is running on
    - **Engine.ReportFont** the font the engine reports are being written in
    - **Engine.TempFilePath** the path where the engine will write temp files
    - **Engine.Type** the type of engine designer is running on
    - **Engine.Version** the version of the engine designer is using
    - **Engine.WorkflowDirectory** the directory of the current workflow
    - **Engine.WorkflowFileName** the file name of the workflow (this is only available if the workflow has been saved)
    - **GlobalRecordLimit** the maximum amount of records designer can process
    - **JupyterTempPath** the temp path Jupyter is writing to
    - **ModuleDirectory** the directory designer module is stored in
    - **OutputConnectionMetaDataMessages** if output connection metadata messages are enabled
    - **PredictiveCodePage** 
    - **ProxyConfiguration** will be used to a proxy network requests
    - **RestrictedDataMode**
    - **RunMode** how the engine interacts with designer
    - **SerialNumber** the serial number for designer
    - **SortedGrouping** 
    - **TempPath** the path to where designer will write temp files
    - **ToolId** the id of the current tool
    - **UpdateOnly** 
    - **UseVfs**
    - **WorkflowDirectory** the directory of the current worklow
    - **WorkflowRunGuid** the guid of the current workflow run

## Usage
Accessing the constants is simple:

    desired_constant = self.provider.environment.*constant*

To access the constants stored in the **_raw_constants** simply do the following:

    desired_constant = self.provider.environment._raw_constants[Engine.*constant*]