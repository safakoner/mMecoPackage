# DESCRIPTION Run unit tests in a package
& $env:MECO_PYTHON_EXECUTABLE_PATH -c "import mMecoPackage.packageCmd;mMecoPackage.packageCmd.runUnitTest()" $args