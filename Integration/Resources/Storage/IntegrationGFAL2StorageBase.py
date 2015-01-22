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

#   def testgetFileSize( self ):
#     # file exists
#     path = '/lhcb/user/p/pgloor/wallpaper.jpg'
#     res = self.tbt.getFileSize( path )
#     self.assertEqual( res['OK'], True )
#     res = res['Value']
#     self.assertEqual( res['Successful'][path], 520484 )
#
#     # file does not exist
#     path = '/lhcb/user/p/pgloor/wallpaper3.jpg'
#     res = self.tbt.getFileSize( path )
#     self.assertEqual( res['OK'], True )
#     res = res['Value']
#     self.assertEqual( res['Failed'][path], "GFAL2StorageBase.__isSingleFile: File does not exist." )
#
#     # path is not a file
#     path = '/lhcb/user/p/pgloor/'
#     res = self.tbt.getFileSize( path )
#     self.assertEqual( res['OK'], True )
#     res = res['Value']
#     self.assertEqual( res['Failed'][path], 'GFAL2StorageBase.__getSingleFileSize: path is not a file' )
#
#     # multi-input
#     path = [ '/lhcb/user/p/pgloor/wallpaper.jpg', '/lhcb/user/p/pgloor/wallpaper3.jpg', '/lhcb/user/p/pgloor/' ]
#     res = self.tbt.getFileSize( path )
#     self.assertEqual( res['OK'], True )
#     res = res['Value']
#     self.assertEqual( res['Successful'][path[0]], 520484 )
#     self.assertEqual( res['Failed'][path[1]], "GFAL2StorageBase.__isSingleFile: File does not exist." )
#     self.assertEqual( res['Failed'][path[2]], 'GFAL2StorageBase.__getSingleFileSize: path is not a file' )
#
#   def testisFile( self ):
#     # file exists
#     path = '/lhcb/user/p/pgloor/wallpaper.jpg'
#     res = self.tbt.isFile( path )
#     self.assertEqual( res['OK'], True )
#     res = res['Value']
#     self.assertEqual( res['Successful'][path], True )
#
#     # file does not exist
#     path = '/lhcb/user/p/pgloor/wallpaper3.jpg'
#     res = self.tbt.isFile( path )
#     self.assertEqual( res['OK'], True )
#     res = res['Value']
#     self.assertEqual( res['Failed'][path], "GFAL2StorageBase.__isSingleFile: File does not exist." )
#
#   def testremoveDirectory( self ):
#     path = '/lhcb/user/p/pgloor/Workflow'
#     res = self.tbt.createDirectory( path )
#     self.assertEqual( res['OK'], True )
#     res = self.tbt.removeDirectory( path, True )
#     self.assertEqual( res['OK'], True )
#     res = res['Value']
#     self.assertAlmostEqual( path in res['Successful'], True )
#     print res

  def atestputGetFolder( self ):
    ########## uploading directory #############
    putDir = { '/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
          '/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }
    listDir = ['/lhcb/user/p/pgloor/Workflow', \
               '/lhcb/user/p/pgloor/Workflow/FolderA', \
               '/lhcb/user/p/pgloor/Workflow/FolderB']
    getDir = [ '/lhcb/user/p/pgloor/Workflow/FolderA', \
               '/lhcb/user/p/pgloor/Workflow/FolderB']
    res = self.tbt.putDirectory( putDir )
    self.assertEqual( res['OK'], True )
    res = self.tbt.listDirectory( listDir )
    print res
    #self.assertEqual( '/lhcb/user/p/pgloor/Workflow/FolderA/FileA' in \
    #              res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys(), True )
    #self.assertEqual( '/lhcb/user/p/pgloor/Workflow/FolderB/FileB' in \
    #                  res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys(), True )

    res = self.tbt.getDirectory( getDir, '/home/phi/dev/UnitTests/getDir' )
    print res

  def testWorkflow( self ):
    putDir = { '/lhcb/user/p/pgloor/Workflow/FolderA' : '/home/phi/dev/UnitTests/FolderA' , \
          '/lhcb/user/p/pgloor/Workflow/FolderB' : '/home/phi/dev/UnitTests/FolderB' }

    createDir = ['/lhcb/user/p/pgloor/Workflow/FolderA/FolderAA']

    putFile = { '/lhcb/user/p/pgloor/Workflow/FolderA/File1' : '/home/phi/dev/UnitTests/File1' , \
                '/lhcb/user/p/pgloor/Workflow/FolderAA/File1': '/home/phi/dev/UnitTest/File1' , \
                '/lhcb/user/p/pgloor/Workflow/FolderBB/File2': '/home/phi/dev/UnitTest/File2' , \
                '/lhcb/user/p/pgloor/Workflow/FolderB/File2' : '/home/phi/dev/UnitTests/File2' , \
                '/lhcb/user/p/pgloor/Workflow/File3' : '/home/phi/dev/UnitTests/File3' }

    isFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']

    listDir = ['/lhcb/user/p/pgloor/Workflow', \
               '/lhcb/user/p/pgloor/Workflow/FolderA', \
               '/lhcb/user/p/pgloor/Workflow/FolderB']

    getDir = [ '/lhcb/user/p/pgloor/Workflow/FolderA', \
           '/lhcb/user/p/pgloor/Workflow/FolderB']

    removeFile = ['/lhcb/user/p/pgloor/Workflow/FolderA/File1']
    rmdir = ['/lhcb/user/p/pgloor/Workflow']

    ########## uploading directory #############
    res = self.tbt.putDirectory( putDir )
    self.assertEqual( res['OK'], True )
    res = self.tbt.listDirectory( listDir )
    self.assertEqual( any('/lhcb/user/p/pgloor/Workflow/FolderA/FileA' in dictKey for dictKey in \
                  res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderA']['Files'].keys() ), True )
    self.assertEqual( any( '/lhcb/user/p/pgloor/Workflow/FolderB/FileB' in dictKey for dictKey in \
                      res['Value']['Successful']['/lhcb/user/p/pgloor/Workflow/FolderB']['Files'].keys() ), True )

    ########## createDir #############
    res = self.tbt.createDirectory( createDir )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( res['Successful'][createDir[0]], True )

    ######## putFile ########
    res = self.tbt.putFile( putFile )
    self.assertEqual( res['OK'], True )

    res = self.tbt.isFile( isFile )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][isFile[0]], True )

    ####### getDirectory ######
    res = self.tbt.getDirectory( getDir, '/home/phi/dev/UnitTests/getDir' )
    self.assertEqual( res['OK'], True )
    res = res['Value']
    self.assertEqual( any( getDir[0] in dictKey for dictKey in res['Successful'] ), True )
    self.assertEqual( any( getDir[1] in dictKey for dictKey in res['Successful'] ), True )

    ###### removeFile ##########
    res = self.tbt.removeFile( removeFile )
    self.assertEqual( res['OK'], True )
    res = self.tbt.exists( removeFile )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][removeFile[0]], False )

    ########### removing directory  ###########
    res = self.tbt.removeDirectory( rmdir, True )
    res = self.tbt.exists( rmdir )
    self.assertEqual( res['OK'], True )
    self.assertEqual( res['Value']['Successful'][rmdir[0]], False )

class SRM2V2Test( basicTest ):

  def setUp( self ):
    basicTest.setUp( self )
    self.tbt = StorageElement( self.storageName, protocols = 'SRM2V2' )


class XROOTTest( basicTest ):

  def setUp( self ):
    basicTest.setUp( self )
    self.tbt = StorageElement( self.storageName, protocols = 'GFAL2_XROOT' )


if __name__ == '__main__':
  # gLogger.setLevel( 'DEBUG' )
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( SRM2V2Test )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( XROOTTest ) )
  unittest.TextTestRunner( verbosity = 2 ).run( suite )
