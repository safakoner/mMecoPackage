#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    mMecoPackage/enumLib.py @brief [ FILE   ] - Enum.
## @package mMecoPackage.enumLib    @brief [ MODULE ] - Enum.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  mMeco.core.enumAbs


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - Name of the files contained by any package.
class PackageFile(mMeco.core.enumAbs.Enum):

    ## [ str ] - Name of readme file.
    kReadMeMarkdownFileName     = 'README.md'

    ## [ str ] - Name of the package environment file.
    kEnvModuleFileBaseName      = 'packageEnvLib'

    ## [ str ] - Name of the package info file that contains information about the package.
    kInfoModuleFileBaseName     = 'packageInfoLib'

    ## [ str ] - Git ignore template file name.
    kGitIgnoreFileBaseName      = 'gitignore'

#
## @brief [ ENUM CLASS ] - Class contains package Python file name suffixes.
class PackagePythonFileSuffix(mMeco.core.enumAbs.Enum):

    ## [ str ] - Abstract.
    kAbs        = 'Abs'

    ## [ str ] - Application info.
    kApp        = 'App'

    ## [ str ] - Configuration.
    kCon        = 'Con'

    ## [ str ] - Container.
    kCnt        = 'Cnt'

    ## [ str ] - Command.
    kCmd        = 'Cmd'

    ## [ str ] - Dependency.
    kDep        = 'Dep'

    ## [ str ] - Dependency list.
    kDepList    = 'DepList'

    ## [ str ] - Graphical User Interface.
    kGui        = 'Gui'

    ## [ str ] - Custom widgets.
    kWidget     = 'Wgt'

    ## [ str ] - Library.
    kLib        = 'Lib'

    ## [ str ] - Test.
    kTest       = 'Test'

    ## [ str ] - Process.
    kPro        = 'Pro'

    ## [ str ] - Process list.
    kProList    = 'ProList'

    ## [ str ] - Examples.
    kEx         = 'Ex'

    ## [ str ] - Exceptions.
    kExc        = 'Exc'

    ## [ str ] - Documentation (Doxygen main page).
    kDoc        = 'Doc'

#
## @brief [ ENUM CLASS ] - Class contains package folder names.
class PackageFolderName(mMeco.core.enumAbs.Enum):

    ## [ str ] - Mac OS platform folder name.
    kDarwin                     = 'darwin'

    ## [ str ] - Linux OS platform folder name.
    kLinux                      = 'linux'

    ## [ str ] - Windows OS platform folder name.
    kWindows                    = 'windows'

    #

    ## [ str ] - Files folder name.
    kFiles                      = 'files'

    ## [ str ] - App folder name.
    kApp                        = 'apps'

    ## [ str ] - Icons folder name.
    kIcons                      = 'icons'

    ## [ str ] - C++ folder name.
    kCPP                        = 'cpp'

    #

    ## [ str ] - Bin (executables) folder name.
    kBin                        = 'bin'

    ## [ str ] - Build folder name.
    kBuild                      = 'build'

    ## [ str ] - Configuration folder name.
    kConfig                     = 'config'

    #

    ## [ str ] - Data folder name.
    kData                       = 'data'

    #

    ## [ str ] - Documentation folder name.
    kDoc                        = 'doc'

    ## [ str ] - Developer folder name.
    kDeveloper                  = 'developer'

    ## [ str ] - User folder name.
    kUser                       = 'user'

    ## [ str ] - C++ API reference folder name.
    kCPPAPIReference            = 'cppAPIReference'

    ## [ str ] - Python API reference folder name.
    kPythonAPIReference         = 'pythonAPIReference'

    ## [ str ] - Reference folder name.
    kReference                  = 'reference'

    #

    ## [ str ] - Houdini folder name.
    kHoudini                    = 'houdini'

    #

    ## [ str ] - Katana folder name.
    kKatana                     = 'katana'

    ## [ str ] - Library folder name.
    kLib                        = 'lib'

    ## [ str ] - Mari folder name.
    kMari                       = 'mari'

    #

    ## [ str ] - Maya folder name.
    kMaya                       = 'maya'

    ## [ str ] - MEL folder name.
    kMEL                        = 'mel'

    ## [ str ] - Plug-in folder name.
    kPlugin                     = 'plugin'

    ## [ str ] - Shelves folder name.
    kShelves                    = 'shelves'

    ## [ str ] - XBM folder name.
    kXBM                        = 'xbm'

    #

    ## [ str ] - Nuke folder name.
    kNuke                       = 'nuke'

    #

    ## [ str ] - Python folder name.
    kPython                     = 'python'

    ## [ str ] - Python unit tests folder name.
    kPythonUnitTestFolderName   = 'tests'

    #

    ## [ str ] - Resource folder name.
    kResources                  = 'resources'

    ## [ str ] - Source folder name for C++, C etc. code.
    kSource                     = 'source'

    ## [ str ] - Temp folder name.
    kTemp                       = 'temp'

    ## [ str ] - Unit test folder name.
    kTest                       = 'test'

#
## @brief [ ENUM CLASS ] - Class contains package folder structure.
class PackageFolderStructure(mMeco.core.enumAbs.Enum):

    ## [ str ] - Bin (executables) path.
    kBin                        = PackageFolderName.kBin

    ## [ str ] - Bin (executables) path on Mac OS.
    kBinDarwin                  = '{}/{}'.format(PackageFolderName.kBin, PackageFolderName.kDarwin)

    ## [ str ] - Bin (executables) path on Linux OS.
    kBinLinux                   = '{}/{}'.format(PackageFolderName.kBin, PackageFolderName.kLinux)

    ## [ str ] - Bin (executables) path on Microsoft Windows OS.
    kBinWindows                 = '{}\\\\{}'.format(PackageFolderName.kBin, PackageFolderName.kWindows)

    #

    ## [ str ] - Build path.
    kBuild                      = PackageFolderName.kBuild

    ## [ str ] - Build path on Mac OS.
    kBuildDarwin                = '{}/{}'.format(PackageFolderName.kBuild, PackageFolderName.kDarwin)

    ## [ str ] - Build path on Linux OS.
    kBuildLinux                 = '{}/{}'.format(PackageFolderName.kBuild, PackageFolderName.kLinux)

    ## [ str ] - Build path on Windows OS.
    kBuildWindows               = '{}\\\\{}'.format(PackageFolderName.kBuild, PackageFolderName.kWindows)

    #

    ## [ str ] - Configuration path.
    kConfig                     = PackageFolderName.kConfig

    #

    ## [ str ] - Data path.
    kData                       = PackageFolderName.kData

    #

    ## [ str ] - Documentation path.
    kDoc                            = PackageFolderName.kDoc

    ## [ str ] - Developer C++ API reference path.
    kDocDeveloperCPPAPIReference    = '{}/{}/{}'.format(PackageFolderName.kDoc, PackageFolderName.kDeveloper, PackageFolderName.kCPPAPIReference)

    ## [ str ] - Developer Python API reference path.
    kDocDeveloperPythonAPIReference = '{}/{}/{}'.format(PackageFolderName.kDoc, PackageFolderName.kDeveloper, PackageFolderName.kPythonAPIReference)

    ## [ str ] - Developer reference path.
    kDocDeveloperReference          = '{}/{}/{}'.format(PackageFolderName.kDoc, PackageFolderName.kDeveloper, PackageFolderName.kReference)

    ## [ str ] - User document path.
    kDocUser                        = '{}/{}'.format(PackageFolderName.kDoc, PackageFolderName.kUser)

    ## [ str ] - User reference document path.
    kDocUserReference               = '{}/{}/{}'.format(PackageFolderName.kDoc, PackageFolderName.kUser, PackageFolderName.kReference)

    #

    ## [ str ] - Houdini path.
    kHoudini                    = PackageFolderName.kHoudini

    #

    ## [ str ] - Katana path.
    kKatana                     = PackageFolderName.kKatana

    #

    ## [ str ] - Library path.
    kLib                        = PackageFolderName.kLib

    ## [ str ] - Library path on Mac OS.
    kLibDarwin                  = '{}/{}'.format(PackageFolderName.kLib, PackageFolderName.kDarwin)

    ## [ str ] - Library path on Linux OS.
    kLibLinux                   = '{}/{}'.format(PackageFolderName.kLib, PackageFolderName.kLinux)

    ## [ str ] - Library path on Windows OS.
    kLibWindows                 = '{}\\\\{}'.format(PackageFolderName.kLib, PackageFolderName.kWindows)

    #

    ## [ str ] - Mari path.
    kMari                       = PackageFolderName.kMari

    #

    ## [ str ] - Maya path.
    kMaya                       = PackageFolderName.kMaya

    ## [ str ] - Maya version path.
    kMayaVersion                = '{}/2020'.format(PackageFolderName.kMaya)

    ## [ str ] - Maya Python path.
    kMayaPython                 = '{}/{}'.format(kMayaVersion, PackageFolderName.kPython)

    ## [ str ] - Maya MEL script path.
    kMayaMEL                    = '{}/{}'.format(kMayaVersion, PackageFolderName.kMEL)

    ## [ str ] - Maya plug-in path.
    kMayaPlugin                 = '{}/{}'.format(kMayaVersion, PackageFolderName.kPlugin)

    ## [ str ] - Maya Mac OS plug-in path.
    kMayaPluginDarwin           = '{}/{}'.format(kMayaPlugin, PackageFolderName.kDarwin)

    ## [ str ] - Maya Linux plug-in path.
    kMayaPluginLinux            = '{}/{}'.format(kMayaPlugin, PackageFolderName.kLinux)

    ## [ str ] - Maya windows plug-in path.
    kMayaPluginWindows          = '{}\\\\{}'.format(kMayaPlugin, PackageFolderName.kWindows)

    ## [ str ] - Maya shelves path.
    kMayaShelves                = '{}/{}'.format(kMayaVersion, PackageFolderName.kShelves)

    ## [ str ] - Maya XMB path.
    kMayaXBM                    = '{}/{}'.format(kMayaVersion, PackageFolderName.kXBM)

    #

    ## [ str ] - Nuke path.
    kNuke                       = PackageFolderName.kNuke

    #

    ## [ str ] - Python path.
    kPython                     = PackageFolderName.kPython

    #

    ## [ str ] - Resource path.
    kResources                  = PackageFolderName.kResources

    ## [ str ] - Files path.
    kResourcesFiles             = '{}/{}'.format(PackageFolderName.kResources, PackageFolderName.kFiles)

    ## [ str ] - App files path.
    kResourcesApp               = '{}/{}'.format(PackageFolderName.kResources, PackageFolderName.kApp)

    ## [ str ] - Icon path.
    kResourcesIcons             = '{}/{}'.format(PackageFolderName.kResources, PackageFolderName.kIcons)

    #

    ## [ str ] - Source directory for C++, C etc. code.
    kSource                     = PackageFolderName.kSource

    ## [ str ] - C++ source path.
    kSourceCPP                  = '{}/{}'.format(PackageFolderName.kSource, PackageFolderName.kCPP)

    ## [ str ] - Source doc path.
    kSourceDoc                  = '{}/{}'.format(PackageFolderName.kSource, PackageFolderName.kDoc)

    ## [ str ] - Source doc developer path.
    kSourceDocDeveloper         = '{}/{}/{}'.format(PackageFolderName.kSource, PackageFolderName.kDoc, PackageFolderName.kDeveloper)

    ## [ str ] - Source doc developer reference path.
    kSourceDocDeveloperReference= '{}/{}/{}/{}'.format(PackageFolderName.kSource,
                                                       PackageFolderName.kDoc,
                                                       PackageFolderName.kDeveloper,
                                                       PackageFolderName.kReference,
                                                       )

    ## [ str ] - Source doc user path.
    kSourceDocUser              = '{}/{}/{}'.format(PackageFolderName.kSource, PackageFolderName.kDoc, PackageFolderName.kUser)

    ## [ str ] - Source doc user reference path.
    kSourceDocUserReference     = '{}/{}/{}/{}'.format(PackageFolderName.kSource,
                                                       PackageFolderName.kDoc,
                                                       PackageFolderName.kUser,
                                                       PackageFolderName.kReference,
                                                       )

    #

    ## [ str ] - Temp path.
    kTemp                       = PackageFolderName.kTemp

    #

    ## [ str ] - Unit test path.
    kTest                       = PackageFolderName.kTest

#
## @brief [ ENUM CLASS ] - Attributes contained by package info module.
class PackageInfoModuleAttribute(mMeco.core.enumAbs.Enum):

    ## [ str ] - Name.
    kName               = 'NAME'

    ## [ str ] - Version.
    kVersion            = 'VERSION'

    ## [ str ] - Description.
    kDescription        = 'DESCRIPTION'

    ## [ list of str ] - Keyword.
    kKeywords           = 'KEYWORDS'

    ## [ list of str ] - Platforms.
    kPlatforms          = 'PLATFORMS'

    ## [ list of dict ] - Documents.
    kDocuments          = 'DOCUMENTS'

    ## [ list of str ] - Applications.
    kApplications       = 'APPLICATIONS'

    ## [ list of str ] - Python versions.
    kPythonVersions     = 'PYTHON_VERSIONS'

    ## [ bool ] - Is active.
    kIsActive           = 'IS_ACTIVE'

    ## [ bool ] - Is external.
    kIsExternal         = 'IS_EXTERNAL'

    ## [ list of str ] - Developers.
    kDevelopers         = 'DEVELOPERS'

    ## [ list of str ] - Dependent packages.
    kDependentPackages  = 'DEPENDENT_PACKAGES'

    ## [ list of str ] - Python packages.
    kPythonPackages     = 'PYTHON_PACKAGES'
