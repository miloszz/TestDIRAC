from DIRAC.Core.Base.Script import parseCommandLine
from symbol import parameters
parseCommandLine()

import unittest
import mock
from DIRAC import gLogger

from DIRAC.Resources.Storage.SRM2V2Storage import SRM2V2Storage
from DIRAC.Resources.Storage.SRM2Storage import SRM2Storage
from DIRAC.Resources.Storage.StorageElement import StorageElement
from DIRAC.Resources.Storage.GFAL2_XROOTStorage import GFAL2_XROOTStorage

class SRM2V2StorageTestCase( unittest.TestCase ):
  """ Test case that sets up with the CERN-GFAL2 storage. Set up uploads 2 files (with gfal2 - not ideal) that will then be attempted to deleted by
      the removefile test.
  """
  def setUp( self ):
    gLogger.setLevel( 'NOTICE' )

    parameters = {}
    storageName = 'CERN-GFAL2'
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='

    self.srmplugin = SRM2V2Storage( storageName, parameters )
    putDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' : \
                '/home/phi/dev/UnitTests/testfiles/bsp.zip', \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg' : \
                '/home/phi/dev/UnitTests/testfiles/wallpaper.jpg' }
    res = self.srmplugin.putFile( putDict )
    if not res['OK']:
      print 'Couldnt upload testfiles to storage - some tests might fail because files are missing'

  def tearDown( self ):
    del self.srmplugin

class SRM2V2StorageTestCaseT( unittest.TestCase ):
  """ Test case that sets up with the CERN-GFAL2 storage. Set up uploads 2 files (with gfal2 - not ideal) that will then be attempted to deleted by
      the removefile test.
  """

  def setUp( self ):
    gLogger.setLevel( 'NOTICE' )
    parameters = {}
    storageName = 'CERN-GFAL2'
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='

    self.srmplugin = SRM2V2Storage( storageName, parameters )

  def tearDown( self ):
    del self.srmplugin



class SRM2StorageTestCase( unittest.TestCase ):

  def setUp( self ):
    gLogger.setLevel( 'NOTICE' )

    parameters = {}
    storageName = 'CERN-GFAL2'
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='

    self.srmplugin = SRM2V2Storage( storageName, parameters )

  def tearDown( self ):
    del self.srmplugin



class SRM2V2StorageTestCaseTape( unittest.TestCase ):
  """ Test case that sets up the CERN-RAW storage for tape operations
  """
  def setUp( self ):
    gLogger.setLevel( 'Notice' )

    parameters = {}
    storageName = 'CERN-GFAL2'
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='

    self.srmplugin = SRM2V2Storage( storageName, parameters )


  def tearDown( self ):
    del self.srm2v2storage



class SRM2V2Storage_FileQueryTests( SRM2V2StorageTestCase ):
  
  def setUp( self ):
    gLogger.setLevel( 'NOTICE' )

    parameters = {}
    storageName = 'CERN-GFAL2'
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='

    self.srmplugin = SRM2V2Storage( storageName, parameters )

  def tearDown( self ):
    del self.srmplugin
#
#   def testExists( self ):
#     # Files exist
#     filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
#                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']
#     res = self.srmplugin.exists( filenames )
#     for filename in filenames:
#       self.assertEqual( res['Value']['Successful'][filename], True )
#
#     # Erroneous filenames
#     Efilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folxder', \
#                   'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Fxolder2']
#     res = self.srmplugin.exists( Efilenames )
#     for filename in Efilenames:
#       self.assertEqual( res['Value']['Successful'][filename], False )
#
#     # Mixed
#     Mfilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
#                   'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Fxolder2']
#     res = self.srmplugin.exists( Mfilenames )
#     self.assertEqual( res['Value']['Successful'][Mfilenames[0]], True )  # exists
#     self.assertEqual( res['Value']['Successful'][Mfilenames[1]], False )  # !exists
#
#
#   def testisFile( self ):
#     filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg', \
#                   'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFile.py']
#     res = self.srmplugin.isFile( filenames )
#     for filename in filenames:
#       self.assertEqual( res['Value']['Successful'][filename], True )
#
#     Efilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/', \
#                    'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFileX.py']
#     res = self.srmplugin.isFile( Efilenames )
#     self.assertEqual( res['Value']['Successful'][Efilenames[0]], False )
#     self.assertEqual( res['Value']['Failed'][Efilenames[1]], "SRM2V2Storage.__isSingleFile: File does not exist." )
#
#     Mfilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg', \
#                    'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFileX.py']
#     res = self.srmplugin.isFile( Mfilenames )
#     self.assertEqual( res['Value']['Successful'][Mfilenames[0]], True )
#     self.assertEqual( res['Value']['Successful'][Mfilenames[1]], False )
#     self.assertEqual( res['Value']['Failed'][Mfilenames[2]], "SRM2V2Storage.__isSingleFile: File does not exist." )
#
#   def testgetFileSize( self ):
#     filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
#                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
#                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg']
#     res = self.srmplugin.getFileSize( filenames )
#     self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
#     self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )
#     self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], "SRM2V2Storage.__isSingleFile: File does not exist." )
#
#   def testgetFileMetadata( self ):
#     filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
#                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
#                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg']
#     res = self.srmplugin.getFileMetadata( filenames )
#     self.assertEqual( res['OK'], True )
#     metaDict = res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip']
#     self.assertEqual( metaDict['File'], True )
#     self.assertEqual( metaDict['Size'], 18850447 )
#     metaDict = res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg']
#     self.assertEqual( metaDict['File'], True )
#     self.assertEqual( metaDict['Size'], 520484 )
#
#     self.assertEqual( res['Value']['Failed'].keys()[0], 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg' )

  def testgetTransportURL( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg']

    res = self.srmplugin.getTransportURL( filenames )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], \
                      'root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' )

    res = self.srmplugin.getTransportURL( filenames, ['gsiftp'] )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], \
                      'gsiftp://eoslhcbftp.cern.ch//eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' )

#     res = self.srmplugin.getTransportURL( filenames, ['root'] )
#     self.assertEqual( res['OK'], True )
#     self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], \
#                       'gsiftp://eoslhcbftp.cern.ch//eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' )


class SRM2V2Storage_putGetTests( SRM2V2StorageTestCase ):
  def testputFile(self):
    putDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' : \
                '/home/phi/dev/UnitTests/testfiles/bsp.zip', \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg' : \
                '/home/phi/dev/UnitTests/testfiles/wallpaper.jpg' }
    res = self.srmplugin.putFile( putDict )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg'], 520484 )

    # 1. Fails: local file does not exist, 2. Succeeds , 3. Fails: source is a directory, not a file
    MputDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp33.zip' :\
                 '/home/phi/dev/UnitTests/testfiles/Folder/a*b.zip' , \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper.jpg' :\
                 '/home/phi/dev/UnitTests/testfiles/TestFolder/Testwallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper2.jpg' :\
                 '/home/phi/dev/UnitTests/testfiles/TestFolder/'  }
    res = self.srmplugin.putFile( MputDict )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp33.zip'], \
                       "SRM2V2Storage.__putFile: The local source file does not exist or is a directory" )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper.jpg'], \
                       520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper2.jpg'], \
                      "SRM2V2Storage.__putFile: The local source file does not exist or is a directory" )

    # 1: Succeeds, 2: Fails: SRM to SRM needs filesize to compare to
    SRMputDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip' : \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' }
    res = self.srmplugin.putFile( SRMputDict, 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip'], 18850447 )
    res = self.srmplugin.putFile( SRMputDict, 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip'], \
                      "SRM2V2Storage.__putFile: For file replication the source file size in bytes must be provided." )

  def testputDirectory( self ):
    dirnames = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1' : '/home/phi/dev/UnitTests/testfiles/TestFolder' , \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2/putDir22' : '/home/phi/dev/UnitTests/testfiles/putDirectoryTest', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir3' : '/home/phi/dev/UnitTests/testfiles/DoenstExist', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir4' : '/home/phi/dev/UnitTests/testfiles/wallpaper.jpg' }
    res = self.srmplugin.putDirectory( dirnames )

    self.assertEqual( res['OK'], True )

    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1']['Files'], 3 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1']['Size'], 19891415 )

    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2/putDir22']['Files'], 5 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2/putDir22']['Size'], 20412870 )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir3']['Files'], 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir3']['Size'], 0 )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir4']['Files'], 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir4']['Size'], 0 )

  def testgetDirectory( self ):
    path = '/home/phi/dev/UnitTests/getDirPath'

    dirnames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1', \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2', \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']
    res = self.srmplugin.getDirectory( dirnames, path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1']['Files'], 3 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1']['Size'], 19891415 )


    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2']['Files'], 5 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2']['Size'], 20412870 )


    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']['Files'], 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']['Size'], 0 )

  def testGetFile( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/' ]
    res = self.srmplugin.getFile( filenames )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], \
                      "SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__isSingleFile: File does not exist." )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/'], \
                      'SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__getSingleFileSize: path is not a file' )

    # with a local path
    res = self.srmplugin.getFile( filenames, '/home/phi/Downloads/getDirTest' )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], \
                      "SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__isSingleFile: File does not exist." )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/'], \
                      'SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__getSingleFileSize: path is not a file' )


class SRM2V2Storage_FileTransferTests( SRM2V2StorageTestCase ):

  def testputFile( self ):
    putDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' : \
                '/home/phi/dev/UnitTests/testfiles/bsp.zip', \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg' : \
                '/home/phi/dev/UnitTests/testfiles/wallpaper.jpg' }
    res = self.srmplugin.putFile( putDict )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg'], 520484 )

    # 1. Fails: local file does not exist, 2. Succeeds , 3. Fails: source is a directory, not a file
    MputDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp33.zip' :\
                 '/home/phi/dev/UnitTests/testfiles/Folder/a*b.zip' , \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper.jpg' :\
                 '/home/phi/dev/UnitTests/testfiles/TestFolder/Testwallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper2.jpg' :\
                 '/home/phi/dev/UnitTests/testfiles/TestFolder/'  }
    res = self.srmplugin.putFile( MputDict )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp33.zip'], \
                       "SRM2V2Storage.__putFile: The local source file does not exist or is a directory" )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper.jpg'], \
                       520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper2.jpg'], \
                      "SRM2V2Storage.__putFile: The local source file does not exist or is a directory" )

    # 1: Succeeds, 2: Fails: SRM to SRM needs filesize to compare to
    SRMputDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip' : \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' }
    res = self.srmplugin.putFile( SRMputDict, 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip'], 18850447 )
    res = self.srmplugin.putFile( SRMputDict, 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip'], \
                      "SRM2V2Storage.__putFile: For file replication the source file size in bytes must be provided." )

  def testGetFile( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/' ]
    res = self.srmplugin.getFile( filenames )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], \
                      "SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__isSingleFile: File does not exist." )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/'], \
                      'SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__getSingleFileSize: path is not a file' )

    # with a local path
    res = self.srmplugin.getFile( filenames, '/home/phi/Downloads/getDirTest' )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], \
                      "SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__isSingleFile: File does not exist." )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/'], \
                      'SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__getSingleFileSize: path is not a file' )

  def testremoveFile( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/' ]
    res = self.srmplugin.removeFile( filenames )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], True )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/'], "SRM2V2Storage.__removeSingleFile: Failed to remove file." )


class SRM2V2Storage_DirectoryTransferTests( SRM2V2StorageTestCase ):

  def testputDirectory( self ):
    dirnames = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1' : '/home/phi/dev/UnitTests/testfiles/TestFolder' , \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2/putDir22' : '/home/phi/dev/UnitTests/testfiles/putDirectoryTest', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir3' : '/home/phi/dev/UnitTests/testfiles/DoenstExist', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir4' : '/home/phi/dev/UnitTests/testfiles/wallpaper.jpg' }
    res = self.srmplugin.putDirectory( dirnames )

    self.assertEqual( res['OK'], True )

    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1']['Files'], 3 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir1']['Size'], 19891415 )

    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2/putDir22']['Files'], 5 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir2/putDir22']['Size'], 20412870 )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir3']['Files'], 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir3']['Size'], 0 )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir4']['Files'], 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/putDir4']['Size'], 0 )

  def testcreateDirectory( self ):
    dirnames = [ 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir', \
              'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir2', \
              'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir', \
              'srm://.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir']
    res = self.srmplugin.createDirectory( dirnames )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir2'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir'], True )
    self.assertEqual( res['Value']['Failed']['srm://.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir'], "SRM2V2Storage.__createSingleDirectory: failed to create directory." )

  def testgetDirectory( self ):
    path = '/home/phi/dev/UnitTests/getDirPath'
    if not path:
      dirnames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']
      res = self.srmplugin.getDirectory( dirnames )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']['Files'], 5 )
      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']['Size'], 20412870 )


      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']['Files'], 5 )
      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']['Size'], 20412870 )


      self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']['Files'], 0 )
      self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']['Size'], 0 )
    else:
      dirnames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']
      res = self.srmplugin.getDirectory( dirnames, path )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']['Files'], 5 )
      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']['Size'], 20412870 )


      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']['Files'], 5 )
      self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']['Size'], 20412870 )


      self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']['Files'], 0 )
      self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']['Size'], 0 )


class SRM2V2Storage_DirectoryQueryTests( SRM2V2StorageTestCase ):
  def testisDirectory( self ):
    dirnames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']
    res = self.srmplugin.isDirectory( dirnames )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], False )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown'], \
                      "SRM2V2Storage.__isSingleDirectory: Directory doesn't exist." )

  def testgetDirectorySize( self ):
    dirnames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']

    res = self.srmplugin.getDirectorySize( dirnames )
    self.assertEqual( res['OK'], True )

    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']['Files'], 3 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']['Size'], 19371902 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']['SubDirs'], 1 )

    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']['Files'], 3 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']['Size'], 19371902 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']['SubDirs'], 1 )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], \
                      'SRM2V2Storage.__listSingleDirectory: could not list directory content.' )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown'], \
                      'SRM2V2Storage.__listSingleDirectory: directory does not exist' )

  def testlistDirectory( self ):
    dirnames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']

    res = self.srmplugin.listDirectory( dirnames )
    self.assertEqual( res['OK'], True )

    self.assertEqual( 'Files' in res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder'].keys(), True )
    self.assertEqual( 'SubDirs' in res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder'].keys(), True )

    self.assertEqual( 'Files' in res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2'].keys(), True )
    self.assertEqual( 'SubDirs' in res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2'].keys(), True )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], \
                      "SRM2V2Storage.listDirectory: path is not a directory" )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown'], \
                      "SRM2V2Storage.__isSingleDirectory: Directory doesn't exist." )


  def testgetDirectoryMetadata( self ):
    dirnames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown']
    res = self.srmplugin.getDirectoryMetadata( dirnames )
    self.assertEqual( res['OK'], True )

    metaDict = res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder']
    self.assertEqual( 'Directory' in metaDict.keys(), True )
    self.assertEqual( metaDict['Directory'], True )

    metaDict = res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']
    self.assertEqual( 'Directory' in metaDict.keys(), True )
    self.assertEqual( metaDict['Directory'], True )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], \
                      "SRM2V2Storage.__getSingleDirectoryMetadata: Provided path is not a directory." )

    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Unknown'], \
                      "SRM2V2Storage.__getSingleMetadata: Path does not exist" )

class SRM2V2Storage_TapeTests( SRM2V2StorageTestCaseTape ):

  def testprestageFileStatus( self ):
    paths_wtoken = { 'srm://srm-lhcb.cern.ch/castor/cern.ch/grid/lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81683/081683_0000000040.raw' : 347447607, \
                     'srm://srm-lhcb.cern.ch/castor/cern.ch/grid/lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81683/081683_0000000041.raw' : 347447610, \
                     'srm://srm-lhcb.cern.ch/castor/cern.ch/grid/lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81683/081683_0000000041x.raw' : 234}
    # broken_path = { 'srm://srm-lhcb.cern.ch/castor/cern.ch/grid/lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81683/081683_0000000041x.raw' : 234}
    res = self.srmplugin.prestageFileStatus( paths_wtoken )

    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-lhcb.cern.ch/castor/cern.ch/grid/lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81683/081683_0000000040.raw'], False )
    self.assertEqual( res['Value']['Successful']['srm://srm-lhcb.cern.ch/castor/cern.ch/grid/lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81683/081683_0000000041.raw'], False )
#
#     res = self.srmplugin.prestageFileStatus( broken_path )
    self.assertEqual( res['Value']['Failed']['srm://srm-lhcb.cern.ch/castor/cern.ch/grid/lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81683/081683_0000000041x.raw'], 'SRM2V2Storage.__prestageSingleFileStatus: Polling request timed out' )


  def testprestageFileMock( self ):
    resource = self.srmplugin
    mock_gfal2 = mock.Mock()
    resource.gfal2 = mock_gfal2

    resource.gfal2.bring_online.return_value = ( 1, 9999 )  # (return code, token)
    path = "A"
    paths = ['A', 'B']
    res = resource.prestageFile( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], 9999 )

    resource.gfal2.bring_online.return_value = ( 0 , 9999 )
    res = resource.prestageFile( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], 9999 )

    resource.gfal2.bring_online.return_value = ( -1 , 9999 )
    res = resource.prestageFile( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Failed']['A'], 'SRM2V2Storage.__prestageSingleFile: an error occured while issuing prestaging.' )

    resource.gfal2.bring_online.side_effect = [( 1, 9999 ), ( 0, 8888 ) ]
    res = resource.prestageFile( paths )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], 9999 )
    self.assertEqual( res['Value']['Successful']['B'], 8888 )

  def testprestageFileStatusMock( self ):
    resource = self.srmplugin
    mock_gfal2 = mock.Mock()
    resource.gfal2 = mock_gfal2

    path = {'A' : 9999}
    paths = {'A' : 9999, 'B' : 8888}

    resource.gfal2.bring_online_poll.return_value = 1
    res = resource.prestageFileStatus( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], True )

    resource.gfal2.bring_online_poll.return_value = 0
    res = resource.prestageFileStatus( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], False )

    resource.gfal2.bring_online_poll.side_effect = [1, 0]
    res = resource.prestageFileStatus( paths )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], True )
    self.assertEqual( res['Value']['Successful']['B'], False )


  def testpinFileMock( self ):
    resource = self.srmplugin
    mock_gfal2 = mock.Mock()
    resource.gfal2 = mock_gfal2

    resource.gfal2.bring_online.return_value = ( 1, 9999 )  # (return code, token)
    path = "A"
    paths = ['A', 'B']
    res = resource.pinFile( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], 9999 )

    resource.gfal2.bring_online.return_value = ( 0 , 9999 )
    res = resource.pinFile( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], 9999 )

    resource.gfal2.bring_online.return_value = ( -1 , 9999 )
    res = resource.pinFile( path )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Failed']['A'], 'SRM2V2Storage.__pinSingleFile: an error occured while issuing pinning.' )

    resource.gfal2.bring_online.side_effect = [( 1, 9999 ), ( 0, 8888 ) ]
    res = resource.pinFile( paths )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['A'], 9999 )
    self.assertEqual( res['Value']['Successful']['B'], 8888 )

  def testreleaseFileMock( self ):
    resource = self.srmplugin
    mock_gfal2 = mock.Mock()
    resource.gfal2 = mock_gfal2

    resource.gfal2.release.side_effect = [1, -1, 0]
    path = { 'A' : 123, 'B' : 456, 'C' : 789 }
    res = resource.releaseFile( path )
    self.assertEqual( res['OK'], True )

    self.assertEqual( res['Value']['Successful']['A'], '123' )
    self.assertEqual( res['Value']['Successful']['B'], '456' )
    self.assertEqual( res['Value']['Failed']['C'], "SRM2V2Storage.__releaseSingleFile: Error occured: Return status < 0" )

class SRM2V2Storage_WorkflowTests( unittest.TestCase ):
  def setUp( self ):
    self.toTest = [SRM2V2Storage]

  def tearDown( self ):
    del self.toTest

  def testWorkflowTest( self ):
    parameters = {}
    storageName = 'CERN-GFAL'
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='

    for cls in self.toTest:

      inst = cls( storageName, parameters )

      putDir = { 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
                'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }

      createDir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/FolderAA']

      putFile = { 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' : '/home/phi/dev/UnitTests/File1' , \
                  'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/File2' : '/home/phi/dev/UnitTests/File2' , \
                  'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/File3' : '/home/phi/dev/UnitTests/File3' }

      isFile = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1']

      listDir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow', \
                 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA', \
                 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB']

      removeFile = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1']

      rmdir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow']


#       putDir = { '/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
#                 '/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }
#
#       createDir = ['/lhcb/user/p/pgloor/Workflow/FolderA/FolderAA']
#
#       putFile = { '/lhcb/user/p/pgloor/Workflow/FolderA/File1' : '/home/phi/dev/UnitTests/File1' , \
#                   '/lhcb/user/p/pgloor/Workflow/FolderB/File2' : '/home/phi/dev/UnitTests/File2' , \
#                   '/lhcb/user/p/pgloor/Workflow/File3' : '/home/phi/dev/UnitTests/File3' }
#
#       isFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']
#
#       listDir = ['/lhcb/user/p/pgloor/Workflow', \
#                  '/lhcb/user/p/pgloor/Workflow/FolderA', \
#                  '/lhcb/user/p/pgloor/Workflow/FolderB']
#
#       removeFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']
#
#       rmdir = ['/lhcb/user/p/pgloor/Workflow']

      inst.putDirectory( putDir )
      res = inst.listDirectory( listDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/FileA' in \
                        res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/FileB' in \
                        res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys(), True )

      ###### putFile ######
      res = inst.putFile( putFile )
      self.assertEqual( res['OK'], True )

      res = inst.isFile( isFile )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][isFile[0]], True )
      ####### putFile for an already existing file #######
      res = inst.putFile( putFile )
      self.assertEqual( res['OK'], True )

      res = inst.isFile( isFile )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][isFile[0]], True )


      ########### listDir after putFile ###########'
      res = inst.listDirectory( listDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' in \
                        res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/File2' in \
                        res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys(), True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/File3' in \
                        res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow']['Files'].keys(), True )
      ########### listDir after removeFile ###########
      res = inst.removeFile( removeFile )
      self.assertEqual( res['OK'], True )

      res = inst.listDirectory( listDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' in \
                        res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), False )

      ########### isDir new Dir ###########
      inst.createDirectory( createDir )
      res = inst.isDirectory( createDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][createDir[0]], True )

      #### Try to create an already existing directory ####
      inst.createDirectory( createDir )
      res = inst.isDirectory( createDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][createDir[0]], True )

      ########### listDir after removing it ###########
      inst.removeDirectory( rmdir, True )
      res = inst.exists( rmdir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][rmdir[0]], False )


class StorageElementTestCase( unittest.TestCase ):
  def setUp( self ):
    self.toTest = [ 'CERN-GFAL2', 'CERN-GFAL' ]

  def tearDown( self ):
    del self.toTest

  def testWorkflowTest( self ):
    parameters = {}
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='
  
    for seName in self.toTest:
      inst = StorageElement( seName )
  
#       putDir = { 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
#                 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }
#   
#       createDir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/FolderAA']
#   
#       putFile = { 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' : '/home/phi/dev/UnitTests/File1' , \
#                   'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/File2' : '/home/phi/dev/UnitTests/File2' , \
#                   'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/File3' : '/home/phi/dev/UnitTests/File3' }
#   
#       isFile = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1']
#   
#       listDir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow', \
#                  'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA', \
#                  'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB']
#   
#       removeFile = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1']
#   
#       rmdir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow']
  

      putDir = { '/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
                '/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }

      createDir = ['/lhcb/user/p/pgloor/Workflow/FolderA/FolderAA']

      putFile = { '/lhcb/user/p/pgloor/Workflow/FolderA/File1' : '/home/phi/dev/UnitTests/File1' , \
                  '/lhcb/user/p/pgloor/Workflow/FolderB/File2' : '/home/phi/dev/UnitTests/File2' , \
                  '/lhcb/user/p/pgloor/Workflow/File3' : '/home/phi/dev/UnitTests/File3' }

      isFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']

      listDir = ['/lhcb/user/p/pgloor/Workflow', \
                 '/lhcb/user/p/pgloor/Workflow/FolderA', \
                 '/lhcb/user/p/pgloor/Workflow/FolderB']

      removeFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']

      rmdir = ['/lhcb/user/p/pgloor/Workflow']
  
      inst.putDirectory( putDir )
      res = inst.listDirectory( listDir )
      print res
      self.assertEqual( res['OK'], True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/FileA' in \
                        res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/FileB' in \
                        res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys(), True )
  
      ###### putFile ######
      res = inst.putFile( putFile )
      self.assertEqual( res['OK'], True )
  
      res = inst.isFile( isFile )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][isFile[0]], True )
      ####### putFile for an already existing file #######
      res = inst.putFile( putFile )
      self.assertEqual( res['OK'], True )
  
      res = inst.isFile( isFile )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][isFile[0]], True )
  
  
      ########### listDir after putFile ###########'
      res = inst.listDirectory( listDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' in \
                        res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/File2' in \
                        res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys(), True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/File3' in \
                        res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow']['Files'].keys(), True )
      ########### listDir after removeFile ###########
      res = inst.removeFile( removeFile )
      self.assertEqual( res['OK'], True )
  
      res = inst.listDirectory( listDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' in \
                        res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), False )
  
      ########### isDir new Dir ###########
      inst.createDirectory( createDir )
      res = inst.isDirectory( createDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][createDir[0]], True )
  
      #### Try to create an already existing directory ####
      inst.createDirectory( createDir )
      res = inst.isDirectory( createDir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][createDir[0]], True )
  
      ########### listDir after removing it ###########
      inst.removeDirectory( rmdir, True )
      res = inst.exists( rmdir )
      self.assertEqual( res['OK'], True )
      self.assertEqual( res['Value']['Successful'][rmdir[0]], False )

class XROOT_GFALTestCase( unittest.TestCase ):
  def setUp( self ):
    parameters = {}
    storageName = 'CERN-GFAL2'
    parameters['Protocol'] = 'root'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/xroot'
    parameters['Host'] = 'eoslhcb.cern.ch'
    parameters['Port'] = ''
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = ''
    self.se = GFAL2_XROOTStorage( storageName, parameters )

  def tearDown( self ):
    del self.se

  def testTransportURL( self ):
    urlToTest1 = ['/lhcb/user/p/pgloor/Folder/wallpaper3.jpg']
    urlToTest2 = 'root://eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg'
    res = self.se.getTransportURL( urlToTest2, 'root' )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][urlToTest2], 'root://eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg' )

class SRM_GFALTestCase( unittest.TestCase ):
  def setUp( self ):
    pass

  def tearDown( self ):
    pass

  def testExists( self ):
    parameters = {}
    storageName = 'CERN-GFAL2'
    parameters['Protocol'] = 'srm'
    parameters['Path'] = '/eos/lhcb/grid/prod/lhcb/gfal2'
    parameters['Host'] = 'srm-eoslhcb.cern.ch'
    parameters['Port'] = '8443'
    parameters['SpaceToken'] = 'LHCb-EOS'
    parameters['Wspath'] = '/srm/v2/server?SFN='
    se = SRM2V2Storage( storageName, parameters )

    putDir = { 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
                'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }

    createDir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/FolderAA']

    putFile = { 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' : '/home/phi/dev/UnitTests/File1' , \
                'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/File2' : '/home/phi/dev/UnitTests/File2' , \
                'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/File3' : '/home/phi/dev/UnitTests/File3' }

    isFile = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1']

    listDir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow', \
               'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA', \
               'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB']

    removeFile = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1']

    rmdir = ['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow']


#       putDir = { '/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
#                 '/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }
#
#       createDir = ['/lhcb/user/p/pgloor/Workflow/FolderA/FolderAA']
#
#       putFile = { '/lhcb/user/p/pgloor/Workflow/FolderA/File1' : '/home/phi/dev/UnitTests/File1' , \
#                   '/lhcb/user/p/pgloor/Workflow/FolderB/File2' : '/home/phi/dev/UnitTests/File2' , \
#                   '/lhcb/user/p/pgloor/Workflow/File3' : '/home/phi/dev/UnitTests/File3' }
#
#       isFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']
#
#       listDir = ['/lhcb/user/p/pgloor/Workflow', \
#                  '/lhcb/user/p/pgloor/Workflow/FolderA', \
#                  '/lhcb/user/p/pgloor/Workflow/FolderB']
#
#       removeFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']
#
#       rmdir = ['/lhcb/user/p/pgloor/Workflow']

    se.putDirectory( putDir )
    res = se.listDirectory( listDir )
    self.assertEqual( res['OK'], True )
    self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/FileA' in \
                      res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), True )
    self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/FileB' in \
                      res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys(), True )

    print 'putFile'
    ###### putFile ######
    res = se.putFile( putFile )
    self.assertEqual( res['OK'], True )

    res = se.isFile( isFile )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][isFile[0]], True )
    ####### putFile for an already existing file #######
    res = se.putFile( putFile )
    self.assertEqual( res['OK'], True )

    res = se.isFile( isFile )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][isFile[0]], True )


    ########### listDir after putFile ###########'
    res = se.listDirectory( listDir )
    self.assertEqual( res['OK'], True )
    self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' in \
                      res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), True )
    self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB/File2' in \
                      res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys(), True )
    self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/File3' in \
                      res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow']['Files'].keys(), True )
    ########### listDir after removeFile ###########
    res = se.removeFile( removeFile )
    self.assertEqual( res['OK'], True )

    res = se.listDirectory( listDir )
    self.assertEqual( res['OK'], True )
    self.assertEqual( 'srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA/File1' in \
                      res['Value']['Successful']['srm://srm-eoslhcb.cern.ch:8443/srm/v2/server?SFN=/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), False )

    ########### isDir new Dir ###########
    se.createDirectory( createDir )
    res = se.isDirectory( createDir )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][createDir[0]], True )

    #### Try to create an already existing directory ####
    se.createDirectory( createDir )
    res = se.isDirectory( createDir )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][createDir[0]], True )

    ########### listDir after removing it ###########
    se.removeDirectory( rmdir, True )
    res = se.exists( rmdir )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][rmdir[0]], False )

if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( SRM_GFALTestCase )
  # suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_FileQueryTests ) )
  # suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_FileTransferTests ) )
  # suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_DirectoryTransferTests ) )
  # suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_DirectoryQueryTests ) )
  # suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_TapeTests ) )
  # suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_WorkflowTests ) )
  unittest.TextTestRunner( verbosity = 2 ).run( suite )

