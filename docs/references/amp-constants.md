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
- **_raw_constants** the rest of the data sent by the engine in it's raw format, currently this consists of two pieces of information:
    - **Engine.WorkflowFileName** the file name of the workflow
    - **Engine.Type** the type of engine

## Usage
Accessing the constants is simple:

    def on_complete(self) -> None:
        desired_constant = self.provider.environment.*constant*

To access the constants stored in the **_raw_constants** simply do the following:

    def on_complete(self) -> None:
        desired_constant = self.provider.environment._raw_constants[Engine.*constant*]