from DIRAC.Core.Base.Script import parseCommandLine
from symbol import parameters
parseCommandLine()

import unittest
from DIRAC import gLogger

from DIRAC.Resources.Storage.StorageElement import StorageElement

class basicTest( unittest.TestCase ):

  def setUp( self ):
    self.storageName = 'CERN-GFAL2'
    self.tbt = None

  def testgetFileSize( self ):
    # file exists
    path = '/lhcb/user/p/pgloor/wallpaper.jpg'
    res = self.tbt.getFileSize( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Successful'][path], 520484 )

    # file does not exist
    path = '/lhcb/user/p/pgloor/wallpaper3.jpg'
    res = self.tbt.getFileSize( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Failed'][path], "GFAL2StorageBase.__isSingleFile: File does not exist." )

    # path is not a file
    path = '/lhcb/user/p/pgloor/'
    res = self.tbt.getFileSize( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Failed'][path], 'GFAL2StorageBase.__getSingleFileSize: path is not a file' )

    # multi-input
    path = [ '/lhcb/user/p/pgloor/wallpaper.jpg', '/lhcb/user/p/pgloor/wallpaper3.jpg', '/lhcb/user/p/pgloor/' ]
    res = self.tbt.getFileSize( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Successful'][path[0]], 520484 )
    self.assertEqual( res['Failed'][path[1]], "GFAL2StorageBase.__isSingleFile: File does not exist." )
    self.assertEqual( res['Failed'][path[2]], 'GFAL2StorageBase.__getSingleFileSize: path is not a file  ' )

  def testisFile( self ):
    # file exists
    path = '/lhcb/user/p/pgloor/wallpaper.jpg'
    res = self.tbt.isFile( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Successful'][path], True )

    # file does not exist
    path = '/lhcb/user/p/pgloor/wallpaper3.jpg'
    res = self.tbt.isFile( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Failed'][path], "GFAL2StorageBase.__isSingleFile: File does not exist." )

    # path is not a file

class SRM2V2Test( basicTest ):

  def setUp( self ):
    basicTest.setUp( self )
    self.tbt = StorageElement( self.storageName, 'SRM2V2' )


class XROOTTest( basicTest ):

  def setUp( self ):
    basicTest.setUp( self )
    self.tbt = StorageElement( self.storageName, 'GFAL2_XROOT' )


if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Test )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( XROOTTest ) )
  unittest.TextTestRunner( verbosity = 2 ).run( suite )
