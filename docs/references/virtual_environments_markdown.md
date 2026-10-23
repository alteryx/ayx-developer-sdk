Virtual Environments
====================

Developing in a Virtual Environment
-----------------------------------

We recommend that you develop your custom plugins inside a virtual
environment. This creates an isolated development environment that
minimizes the risk of creating a package that Alteryx Designer and other
users won't be able to use. To do this, it keeps the dependencies
required by different projects separate.

Workspace Setup
---------------

Make sure to create a new virtual environment with Python version 3.13
before you initialize your SDK workspace. Install [Python
3.13](https://www.python.org/downloads/) if you haven't already. Create
and activate the environment (named `<env_name>`) using one of these
methods:

-   **Command line:**
    -   Verify that `python` resolves to a 3.13.x installation:
        `python --version`.
    -   If you have multiple Python versions installed and the
        default `python` isn't 3.13.x, run `where python` to list
        every installation on your `PATH`, then run
        `<path>\python.exe --version` on each until you find the one
        reporting 3.13.x.
    -   Create the environment with that interpreter:
        `python -m venv <env_name>` (or
        `"<path-to-python3.13>\python.exe" -m venv <env_name>` if you
        had to disambiguate above).
    -   Activate it with `<env_name>\Scripts\activate`.
-   **VSCode:**
    -   Open the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`), and
        run **Python: Create Environment**.
    -   Select **Venv**, and choose your Python 3.13 interpreter from
        the list (VSCode shows the version next to each interpreter,
        so this works even with multiple installs).
    -   VSCode creates the environment and activates it as the
        workspace interpreter.
    -   To activate an existing environment instead of creating a new
        one, open the Command Palette, run **Python: Select
        Interpreter**, and choose the venv's `python.exe` (for
        example, `<env_name>\Scripts\python.exe`).
-   **PyCharm:**
    -   If you're starting a new PyCharm project, you can create the
        environment directly from the **New Project** screen: set
        **Interpreter type** to **Project venv**, choose your Python
        3.13 version from the dropdown, and click **Create**. PyCharm
        creates the venv in the project root and sets it as the
        project interpreter.
    -   For an existing project, go to **Settings** \> **Project** \>
        **Python Interpreter** \> **Add Interpreter** \> **Add Local
        Interpreter** \> **Virtualenv Environment** (New).
    -   Choose your Python 3.13 interpreter as the base (PyCharm lists
        the version for each), and confirm.
    -   PyCharm creates the environment and sets it as the project
        interpreter.
    -   To activate an existing environment instead, use **Add
        Interpreter** \> **Add Local Interpreter** \> **Virtualenv
        Environment** \> **Existing**, and select the `python`
        executable inside it.

3rd-party Packages
------------------

During development, if you need 3rd-party dependencies for your custom
plugin, make sure to add these requirements to the
`requirements-thirdparty.txt` file. You should add any locally-created
packages that become dependencies to the `requirements-local.txt` file.

Best Practices
--------------

Your virtual environment should only include libraries that help you
develop the plugin. Make sure to remove libraries that were installed
but not used. This ensures a clean list of dependencies for installs on
end-user systems. List any packages that are explicitly imported or
required by the plugin in `requirements-thirdparty.txt`.

In general, anytime you use `pip install` to add a dependency to your
plugin, you should update the `requirements-thirdparty.txt` file. To
automatically generate a requirements file for all packages that are
part of the current virtual environment, use the
`pip freeze > list-of-requirements.txt` command.

You will need to prune this file to remove any dependencies that aren\'t
explicitly imported or required by your plugin. Do this before you
copy/overwrite the contents to the `requirements-thirdparty.txt` file
that is created as part of the workspace initialization. The file exists
under `/backend/requirements-thirdparty.txt`.
