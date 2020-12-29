# DESCRIPTION Create a python module for a python package
& $env:MECO_PYTHON_EXECUTABLE_PATH -c "import mMecoPackage.packageCmd;mMecoPackage.packageCmd.createPythonModule()" $args