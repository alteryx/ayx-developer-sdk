Virtual Environments
====================

Developing in a Virtual Environment
-----------------------------------

We recommend that you develop your custom plugins inside a virtual
environment. This creates an isolated development environment that
minimizes the risk of creating a package that Alteryx Designer and other
users won\'t be able to use. It does this by keeping the dependencies
required by different projects separate.

Workspace Setup
---------------

Make sure to create a new virtual environment with Python version 3.8
before you initialize your SDK workspace. With Conda, the command is
`conda create --name <env_name>`.

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
