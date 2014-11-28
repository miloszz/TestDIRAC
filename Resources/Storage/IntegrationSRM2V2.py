from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()

import unittest

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

  def tearDown( self ):
    del self.srm2v2storage


class SRM2V2Storage_Success( SRM2V2StorageTestCase ):
  def testExists( self ):
    # Files exist
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2']
    res = self.srm2v2storage.exists( filenames )
    for filename in filenames:
      self.assertEqual( res['Value']['Successful'][filename], True )

    # Erroneous filenames
    Efilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folxder', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Fxolder2']
    res = self.srm2v2storage.exists( Efilenames )
    for filename in Efilenames:
      self.assertEqual( res['Value']['Successful'][filename], False )

    # Mixed
    Mfilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Fxolder2']
    res = self.srm2v2storage.exists( Mfilenames )
    self.assertEqual( res['Value']['Successful'][Mfilenames[0]], True )  # exists
    self.assertEqual( res['Value']['Successful'][Mfilenames[1]], False )  # !exists


  def testisFile( self ):
    filenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFile.py']
    res = self.srm2v2storage.isFile( filenames )
    for filename in filenames:
      self.assertEqual( res['Value']['Successful'][filename], True )

    Efilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFileX.py']
    res = self.srm2v2storage.isFile( Efilenames )
    self.assertEqual( res['Value']['Successful'][Efilenames[0]], False )
    self.assertEqual( res['Value']['Failed'][Efilenames[1]], "SRM2V2Storage.__isSingleFile: File does not exist." )

    Mfilenames = ['srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/wallpaper3.jpg', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder/', 'srm://srm-eoslhcb.cern.ch/eos/lhcb/grid/prod/lhcb/gfal2/lhcb/user/p/pgloor/Folder2/TestUploadFileX.py']
    res = self.srm2v2storage.isFile( Mfilenames )
    self.assertEqual( res['Value']['Successful'][Mfilenames[0]], True )
    self.assertEqual( res['Value']['Successful'][Mfilenames[1]], False )
    self.assertEqual( res['Value']['Failed'][Mfilenames[2]], "SRM2V2Storage.__isSingleFile: File does not exist." )



if __name__ == '__main__':


  suite = unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2StorageTestCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Storage_Success ) )
  unittest.TextTestRunner( verbosity = 2 ).run( suite )
