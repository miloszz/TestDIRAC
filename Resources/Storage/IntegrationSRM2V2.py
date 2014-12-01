from DIRAC.Core.Base.Script import parseCommandLine
from mock import MagicMock
parseCommandLine()

import unittest
import mock

from DIRAC import gLogger

from DIRAC.Resources.Storage.SRM2V2Storage import SRM2V2Storage


class SRM2V2StorageTestCase( unittest.TestCase ):

  def setUp( self ):
    gLogger.setLevel( 'NOTICE' )


    storageName = 'CERN-GFAL2'
    protocol = 'srm'
    path = '/eos/lhcb/grid/prod/lhcb/gfal2'
    host = 'srm-eoslhcb.cern.ch'
    port = '8443'
    spaceToken = 'LHCb-EOS'
    wspath = '/srm/v2/server?SFN='

    self.srm2v2storage = SRM2V2Storage( storageName, protocol, path, host, port, spaceToken, wspath )
    putDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' : \
                '/home/phi/dev/UnitTests/testfiles/bsp.zip', \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg' : \
                '/home/phi/dev/UnitTests/testfiles/wallpaper.jpg' }
    res = self.srm2v2storage.putFile( putDict )
#     gfal2_mock = mock.Mock()
#     self.srm2v2storage.gfal2 = gfal2_mock
    if not res['OK']:
      print 'Couldnt upload testfiles to storage - some tests might fail because files are missing'

  def tearDown( self ):
    del self.srm2v2storage



class SRM2V2Storage_FileQueryTests( SRM2V2StorageTestCase ):

  def testExists( self ):
    # Files exist
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']
    res = self.srm2v2storage.exists( filenames )
    for filename in filenames:
      self.assertEqual( res['Value']['Successful'][filename], True )

    # Erroneous filenames
    Efilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folxder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Fxolder2']
    res = self.srm2v2storage.exists( Efilenames )
    for filename in Efilenames:
      self.assertEqual( res['Value']['Successful'][filename], False )

    # Mixed
    Mfilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Fxolder2']
    res = self.srm2v2storage.exists( Mfilenames )
    self.assertEqual( res['Value']['Successful'][Mfilenames[0]], True )  # exists
    self.assertEqual( res['Value']['Successful'][Mfilenames[1]], False )  # !exists


  def testisFile( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg', \
                  'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFile.py']
    res = self.srm2v2storage.isFile( filenames )
    for filename in filenames:
      self.assertEqual( res['Value']['Successful'][filename], True )

    Efilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/', \
                   'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFileX.py']
    res = self.srm2v2storage.isFile( Efilenames )
    self.assertEqual( res['Value']['Successful'][Efilenames[0]], False )
    self.assertEqual( res['Value']['Failed'][Efilenames[1]], "SRM2V2Storage.__isSingleFile: File does not exist." )

    Mfilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg', \
                   'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFileX.py']
    res = self.srm2v2storage.isFile( Mfilenames )
    self.assertEqual( res['Value']['Successful'][Mfilenames[0]], True )
    self.assertEqual( res['Value']['Successful'][Mfilenames[1]], False )
    self.assertEqual( res['Value']['Failed'][Mfilenames[2]], "SRM2V2Storage.__isSingleFile: File does not exist." )

  def testgetFileSize( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg']
    res = self.srm2v2storage.getFileSize( filenames )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], "SRM2V2Storage.__isSingleFile: File does not exist." )

  def testgetFileMetadata( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg']
    res = self.srm2v2storage.getFileMetadata( filenames )
    self.assertEqual( res['OK'], True )
    metaDict = res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip']
    self.assertEqual( metaDict['File'], True )
    self.assertEqual( metaDict['Size'], 18850447 )
    metaDict = res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg']
    self.assertEqual( metaDict['File'], True )
    self.assertEqual( metaDict['Size'], 520484 )

    self.assertEqual( res['Value']['Failed'].keys()[0], 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg' )

  def testgetTransportURL( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg']

    res = self.srm2v2storage.getTransportURL( filenames )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], \
                      'root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' )

    res = self.srm2v2storage.getTransportURL( filenames, ['gsiftp'] )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], \
                      'gsiftp://eoslhcbftp.cern.ch//eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' )

#     res = self.srm2v2storage.getTransportURL( filenames, ['root'] )
#     self.assertEqual( res['OK'], True )
#     self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], \
#                       'gsiftp://eoslhcbftp.cern.ch//eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' )


class SRM2V2Storage_FileTransferTests( SRM2V2StorageTestCase ):

  def testputFile( self ):
    putDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' : \
                '/home/phi/dev/UnitTests/testfiles/bsp.zip', \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg' : \
                '/home/phi/dev/UnitTests/testfiles/wallpaper.jpg' }
    res = self.srm2v2storage.putFile( putDict )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )

    # 1. Fails: local file does not exist, 2. Succeeds , 3. Fails: source is a directory, not a file
    MputDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp33.zip' :\
                 '/home/phi/dev/UnitTests/testfiles/Folder/a*b.zip' , \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper.jpg' :\
                 '/home/phi/dev/UnitTests/testfiles/TestFolder/Testwallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper2.jpg' :\
                 '/home/phi/dev/UnitTests/testfiles/TestFolder/'  }
    res = self.srm2v2storage.putFile( MputDict )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp33.zip'], \
                       "SRM2V2Storage.__putFile: The local source file does not exist or is a directory" )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper.jpg'], \
                       520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/DoesntExist/wallpaper2.jpg'], \
                      "SRM2V2Storage.__putFile: The local source file does not exist or is a directory" )

    # 1: Succeeds, 2: Fails: SRM to SRM needs filesize to compare to
    SRMputDict = { 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip' : \
                'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip' }
    res = self.srm2v2storage.putFile( SRMputDict, 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip'], 18850447 )
    res = self.srm2v2storage.putFile( SRMputDict, 0 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp2.zip'], \
                      "SRM2V2Storage.__putFile: For file replication the source file size in bytes must be provided." )

  def testGetFile( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg', \
                 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/' ]
    res = self.srm2v2storage.getFile( filenames )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], 18850447 )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], 520484 )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], \
                      "SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__isSingleFile: File does not exist." )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/'], \
                      'SRM2V2Storage.__getSingleFile: Error while determining file size: SRM2V2Storage.__getSingleFileSize: path is not a file' )

    # with a local path
    res = self.srm2v2storage.getFile( filenames, '/home/phi/Downloads/getDirTest' )
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
    res = self.srm2v2storage.removeFile( filenames )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/bsp.zip'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/wallpaper.jpg'], True )
    self.assertEqual( res['Value']['Successful']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/doesntexist.jpg'], True )
    self.assertEqual( res['Value']['Failed']['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/'], "SRM2V2Storage.__removeSingleFile: Failed to remove file." )


class SRM2V2Storage_DirectoryTransferTests( SRM2V2StorageTestCase ):
  def testcreateDirectory( self ):
    dirnames = [ 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir', \
              'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir2', \
              'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir', \
              'srm://.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/createDirTest/SubDir']
    res = self.srm2v2storage.createDirectory( dirnames )
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
      res = self.srm2v2storage.getDirectory( dirnames )
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
      res = self.srm2v2storage.getDirectory( dirnames, path )
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
    res = self.srm2v2storage.isDirectory( dirnames )
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

    res = self.srm2v2storage.getDirectorySize( dirnames )
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

    res = self.srm2v2storage.listDirectory( dirnames )
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
    res = self.srm2v2storage.getDirectoryMetadata( dirnames )
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

class SRM2V2Storage_preStageTests( SRM2V2StorageTestCase ):
  pass

if __name__ == '__main__':


  suite = unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2StorageTestCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_FileQueryTests ) )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_FileTransferTests ) )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_DirectoryTransferTests ) )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_DirectoryQueryTests ) )
  unittest.TextTestRunner( verbosity = 2 ).run( suite )

