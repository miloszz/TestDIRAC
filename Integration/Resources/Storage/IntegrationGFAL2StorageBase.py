from DIRAC.Core.Base.Script import parseCommandLine
from symbol import parameters
parseCommandLine()

import unittest
from DIRAC import gLogger

from DIRAC.Resources.Storage.StorageElement import StorageElement

class basicTest( unittest.TestCase ):

  def setUp( self ):
    print "in the base"
    self.storageName = 'CERN-GFAL2'
    self.tbt = None

  def testgetFileSize( self ):
    path = '/lhcb/user/p/pgloor/wallpaper.jpg'
    res = self.tbt.getFileSize( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Successful'][path], 520484 )

    path = '/lhcb/user/p/pgloor/wallpaper3.jpg'
    res = self.tbt.getFileSize( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Failed'][path], "GFAL2StorageBase.__isSingleFile: File does not exist." )

    path = '/lhcb/user/p/pgloor/'
    res = self.tbt.getFileSize( path )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Failed'][path], 'GFAL2StorageBase.__getSingleFileSize: path is not a file' )



class SRM2V2Test( basicTest ):

  def setUp( self ):
    print "xtest"
    basicTest.setUp( self )
    self.tbt = StorageElement( self.storageName, 'SRM2V2' )
    # TODO: set pluginName to SRM2V2


class XROOTTest( basicTest ):

  def setUp( self ):
    print "ytest"
    basicTest.setUp( self )
    self.tbt = StorageElement( self.storageName, 'GFAL2_XROOT' )
    # TODO: set pluginName to GFAL2_XROOT

if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Test )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( XROOTTest ) )
  unittest.TextTestRunner( verbosity = 2 ).run( suite )
