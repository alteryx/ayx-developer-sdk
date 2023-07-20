# Debugging SDK Tools
Now that you've built your first SDK Tool, you want to confirm that it's properly installed and that the code you've written is being executed. This guide will show you places to check for correctness and how to verify that your plugin is being correctly built and executed. It is recommended to follow these steps when behavior is not acting as expected, and to always rebuild using the `create-yxi` command to iterate and ensure that changes are being made to your plugin code.  


## Table of Contents
1. After `create-yxi`
2. After installing `.yxi`
3. After running in Designer
4. Running the plugin at Command Line
5. Simple ways to print/check values


## 1. After `create-yxi`
After creating the yxi, there will be a new folder in your workspace called `build`. Navigate to `~/your_tool_workspace/build/yxi/workspace_name.yxi` and rename the `.yxi` to a `.zip` archive. 

Inside the archive, navigate to `<TOOL_NAME>/site-packages/ayx_plugins/<tool_name>.py`. When opening this file, you should expect to see the exact same code as the plugin code in your tool workspace (`~/your_tool_workspace/backend/ayx_plugins/<tool_name>.py`). If you make some changes to your code in your workspace, all updates should also propogate to this file that's in the `.yxi` that you build. This step is used to confirm that the `.yxi` is being built with the correct code and dependencies. You can verify that the other plugin dependencies are also being correctly built by simply searching for that dependency in the `site-packages` folder of the archive. 

## 2. After installing `.yxi`
After installing the `.yxi`, there will be a new folder created that can be found in `~/%APPDATA%/Roaming/Alteryx/Tools/<TOOL_NAME>` directory for user installs. (For admin installs, please check your Alteryx system installation folder) 

In the created tool folder, navigate to `/site-packages/ayx_plugins/<tool_name>.py`. When opening this file, you should expect to see the exact same code as the plugin code in your tool workspace (`~/your_tool_workspace/backend/ayx_plugins/<tool_name>.py`). To reiterate, when you make some changes to your code in your workspace, recreate and install the `.yxi`, you should expect the same changes to also propogate to this file in the installed tool folder. These checks will confirm that the installation process is working correctly.

## 3. After running in Designer
If, after you've run the plugin in Designer, the tool does not yield expected results, you can check the logs following this method:

Checking for PythonSDK.log and enabling Debug logging:

- Tool logs are written to a file called PythonSDK.log located in Local AppData. For example, `%LOCALAPPDATA%\Alteryx\Log\PythonSDK.log`.

- Ensure you launch the plugin with the environment variable 
`AYX_SDK_VERBOSE=1`.
For example, one way to do this is in the Windows Environment dialog. Windows 10+ users, go to [How Do I Set System Environment Variables in Windows 10](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10_E) for more information.

For more, please see the [FAQ](https://github.com/alteryx/ayx-developer-sdk/blob/main/docs/references/faq.md#where-are-the-debug-logs-located)

By checking the logs, you will see what is happening during execution time and be able to check your expectations of what you think should be happening with what is actually happening. 


## 4. Running the plugin at command line
If you see an error message that looks like `Internal error: Failed to read port assignment`, you can try to run the `main.pyz` from your tool workspace using the command line to diagnose the error that's preventing the port assignment. Navigate to your tool workspace and run the following command:

`python main.pyz start-sdk-tool-service ayx_plugins <tool_name>`
A successful run will look like this:

```sh
(dev) orion.ou ~\tool_workspace [11:54AM]> python .\main.pyz start-sdk-tool-service ayx_plugins Passthrough
ListenPort: None
INFO: Starting shivRemoval tool with AMP Provider.
ListenPort: 62136
```

If there are any issues with your python code, it would look something like this:

```sh
(dev) orion.ou ~\post-shiv-removal [01:08PM]> python .\main.pyz start-sdk-tool-service ayx_plugins shivRemoval
ListenPort: None
INFO: Starting shivRemoval tool with AMP Provider.
EXCEPTION: name 'badcode' is not defined
Traceback (most recent call last):
  File ".\main.pyz", line 39, in <module>
    start_sdk_tool_service(tool_package, tool_name, os.getenv("TOOL_SERVICE_ADDRESS"))
  File "c:\users\orion.ou\sdks\ayx-core\ayxsdk\ayxpythonsdk\ayx_python_sdk\providers\amp_provider\__main__.py", line 48, in start_sdk_tool_service
    plugin_class = load_plugin_class(plugins_package, tool_name)
  File "c:\users\orion.ou\sdks\ayx-core\ayxsdk\ayxpythonsdk\ayx_python_sdk\providers\amp_provider\plugin_class_loader.py", line 62, in load_plugin_class
    plugins_module = importlib.import_module(plugins_package)
  File "C:\Users\orion.ou\Miniconda3\envs\dev\lib\importlib\__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
  File "<frozen importlib._bootstrap>", line 991, in _find_and_load
  File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 671, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 783, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "C:\Users\orion.ou\workspaces\post-shiv-removal\.ayx_cli.cache\dist\ayx_plugins\__init__.py", line 15, in <module>
    from .shiv_removal import shivRemoval
  File "C:\Users\orion.ou\workspaces\post-shiv-removal\.ayx_cli.cache\dist\ayx_plugins\shiv_removal.py", line 21, in <module>
    badcode
NameError: name 'badcode' is not defined
```

## 5. Simple ways to print/check values
In your plugin code, use the `self.provider.io.info("")` method to add output to your tool that will show up in Designer. This is an easy and simple way to look at order in which your code is executing in live runs of the plugin. Using this method is a bit more convenient than using python's `println()` method since you would have to check the `PythonSDK.log` to see those print statements. 