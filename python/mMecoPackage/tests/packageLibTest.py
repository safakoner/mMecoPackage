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
## @file    mMecoPackage/tests/packageLibTest.py [ FILE   ] - Unit test module.
## @package mMecoPackage.tests.packageLibTest    [ MODULE ] - Unit test module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import shutil
import unittest

import mMecoPackage.packageLib
import mMecoPackage.enumLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
class PackageTest(unittest.TestCase):

    def setUp(self):

        self._testPackageName = 'testPackage'
        self._packageName  = 'mMecoPackage'
        self._packagesPath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                          '..',
                                                          '..',
                                                          '..',
                                                          '..')
                                             )

        self._packageRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                         '..',
                                                         '..',
                                                         '..')
                                            )

        self._packageName = os.path.basename(self._packageRoot)

        self._packageInfoModuleFilePath = os.path.join(self._packageRoot,
                                                       mMecoPackage.enumLib.PackageFolderName.kPython,
                                                       self._packageName,
                                                       '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName)
                                                       )

    def tearDown(self):

        testPackagePath = os.path.join(self._packagesPath, self._testPackageName)
        if os.path.isdir(testPackagePath):
            shutil.rmtree(testPackagePath)

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    def test_create(self):

        package = mMecoPackage.packageLib.Package.create(name=self._testPackageName,
                                                         description='This is a test package.',
                                                         path=self._packagesPath,
                                                         external=False)

        self.assertEqual(package.version(), '1.0.0')

    def test_set(self):

        package = mMecoPackage.packageLib.Package()

        self.assertTrue(package.setPackage(__file__))

        self.assertEqual(package.name(), self._packageName)

        self.assertTrue(package.setPackage(os.path.join(self._packageRoot,
                                                        mMecoPackage.enumLib.PackageFolderName.kPython,
                                                        self._packageName,
                                                        mMecoPackage.enumLib.PackageFolderName.kPythonUnitTestFolderName)
                                           )
                        )

        self.assertEqual(package.name(), self._packageName)

        self.assertTrue(package.setPackage(os.path.join(self._packageRoot,
                                                        mMecoPackage.enumLib.PackageFolderName.kPython,
                                                        self._packageName,
                                                        mMecoPackage.enumLib.PackageFolderName.kPythonUnitTestFolderName,
                                                        '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName)
                                                        )
                                           )
                        )

        self.assertEqual(package.name(), self._packageName)

        package = mMecoPackage.packageLib.Package(__file__)

        self.assertEqual(package.name(), self._packageName)

    #
    # ------------------------------------------------------------------------------------------------
    # RELEASE
    # ------------------------------------------------------------------------------------------------
    def test_getPackageReleaseRelativePath(self):

        package = mMecoPackage.packageLib.Package(self._packageRoot)

        self.assertEqual(package.getPackageReleaseRelativePath(),
                         '{}/{}/{}'.format(self._packageName,
                                           package.version(),
                                           self._packageName))

    #
    # ------------------------------------------------------------------------------------------------
    # CONTENT
    # ------------------------------------------------------------------------------------------------
    def test_getPythonPackages(self):

        package = mMecoPackage.packageLib.Package(self._packageRoot)

        self.assertEqual(package.getPythonPackages(),
                         ['mMecoPackage'])

    def test_getLocalDocument(self):

        package = mMecoPackage.packageLib.Package(self._packageRoot)

        self.assertEqual(package.getLocalDocument(mMecoPackage.enumLib.PackageFolderStructure.kDocDeveloperCPPAPIReference),
                         None)

    #
    # ------------------------------------------------------------------------------------------------
    # LOCATION
    # ------------------------------------------------------------------------------------------------
    def test_getLocation(self):

        package = mMecoPackage.packageLib.Package(self._packageRoot)

        self.assertEqual(package.getLocation(),
                         self._packagesPath)

    def test_getPythonPath(self):

        package = mMecoPackage.packageLib.Package(self._packageRoot)

        self.assertEqual(package.getPythonPath(),
                         os.path.join(self._packageRoot,
                                      mMecoPackage.enumLib.PackageFolderName.kPython,
                                      )
                         )

    def test_getPythonPackagePath(self):

        package = mMecoPackage.packageLib.Package(self._packageRoot)

        self.assertEqual(package.getPythonPackagePath(),
                         os.path.join(self._packageRoot,
                                      mMecoPackage.enumLib.PackageFolderName.kPython,
                                      package.name())
                         )


    def test_getLocalPath(self):

        package = mMecoPackage.packageLib.Package(self._packageRoot)

        self.assertEqual(package.getLocalPath(mMecoPackage.enumLib.PackageFolderStructure.kBinDarwin),
                         os.path.join(self._packageRoot,
                                      mMecoPackage.enumLib.PackageFolderName.kBin,
                                      mMecoPackage.enumLib.PackageFolderName.kDarwin
                                      )
                         )

    #
    # ----------------------------------------------------------------------------------------------------
    # QUERY
    # ----------------------------------------------------------------------------------------------------
    def test_isRootOfAPackage(self):

        self.assertTrue(mMecoPackage.packageLib.Package.isRootOfAPackage(self._packageRoot))

    def test_isInfoModuleFile(self):

        self.assertEqual(mMecoPackage.packageLib.Package.isInfoModuleFile(self._packageInfoModuleFilePath),
                         self._packageRoot)

    #
    # ----------------------------------------------------------------------------------------------------
    # DISCOVER
    # ----------------------------------------------------------------------------------------------------
    def test_getPackageName(self):

        self.assertEqual(mMecoPackage.packageLib.Package.getPackageName(self._packageInfoModuleFilePath),
                         self._packageName)

    def test_getInfoModuleFile(self):

        packageInfoModuleFile = mMecoPackage.packageLib.Package.getInfoModuleFile(self._packageRoot)

        self.assertTrue(packageInfoModuleFile.endswith('/development/main/mMecoPackage/python/mMecoPackage/packageInfoLib.py'))

        #

        nonPackagePath = os.path.abspath(os.path.join(self._packageRoot, '..', 'noPackage'))

        self.assertIsNone(mMecoPackage.packageLib.Package.getInfoModuleFile(nonPackagePath))

    def test_getPackageByImport(self):

        self.assertTrue(isinstance(mMecoPackage.packageLib.Package.getPackageByImport('{}.packageInfoLib'.format(self._packageName)),
                                   mMecoPackage.packageLib.Package))

        self.assertIsNone(mMecoPackage.packageLib.Package.getPackageByImport('NoSuchPackage.packageInfoLib'))

    def test_list(self):

        self.assertNotEqual(len(mMecoPackage.packageLib.Package.list()), 0)

#
#-----------------------------------------------------------------------------------------------------
# INVOKE
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    unittest.main()
