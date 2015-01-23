""" This is a test of the chain
    FileCatalogClient -> FileCatalogHandler -> FileCatalogDB

    It supposes that the DB is present, and that the service is running
"""

import unittest


from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()


seName = "mySE"
testUser = 'atsareg'
testGroup = 'dirac_user'
testDir = '/vo.formation.idgrilles.fr/user/a/atsareg/testdir'
parentDir = '/vo.formation.idgrilles.fr/user/a/atsareg'
nonExistingDir = "/I/Dont/exist/dir"
testFile = '/vo.formation.idgrilles.fr/user/a/atsareg/testdir/testfile'
nonExistingFile = "/I/Dont/exist"


class DFCTestCase(unittest.TestCase):

  def setUp( self ):
#     gLogger.setLevel( "DEBUG" )

    self.dfc = FileCatalogClient( "DataManagement/FileCatalog" )







class UserGroupCase( DFCTestCase ):

  def test_userOperations( self ):
    """Testing the user related operations"""

    # Add the user
    result = self.dfc.addUser( testUser )
    self.assert_( result['OK'], "AddUser failed when adding new user: %s" % result )
    # Add an existing user
    result = self.dfc.addUser( testUser )
    self.assert_( result['OK'], "AddUser failed when adding existing user: %s" % result )
    # Fetch the list of user
    result = self.dfc.getUsers()
    self.assert_( result['OK'], "getUsers failed: %s" % result )
    # Check if our user is present
    self.assert_( testUser in result['Value'], "getUsers failed: %s" % result )
    # remove the user we created
    result = self.dfc.deleteUser( testUser )
    self.assert_( result['OK'], "deleteUser failed: %s" % result )


  def test_groupOperations( self ):
    """Testing the group related operations"""

    # Create new group
    result = self.dfc.addGroup( testGroup )
    self.assert_( result['OK'], "AddGroup failed when adding new user: %s" % result )
    result = self.dfc.addGroup( testGroup )
    self.assert_( result['OK'], "AddGroup failed when adding existing user: %s" % result )
    result = self.dfc.getGroups()
    self.assert_( result['OK'], "getGroups failed: %s" % result )
    self.assert_( testGroup in result['Value'] )
    result = self.dfc.deleteGroup( testGroup )
    self.assert_( result['OK'], "deleteGroup failed: %s" % result )




class FileCase( DFCTestCase ):

  def test_fileOperations( self ):
    """
      Tests the File related Operations
      this test requires the SE to be properly defined in the CS -> NO IT DOES NOT!!
    """
    # Adding a new file
    result = self.dfc.addFile( { testFile: { 'PFN': 'testfilePFN',
                                         'SE': 'testSE' ,
                                         'Size':123,
                                         'GUID':1000,
                                         'Checksum':'0' } } )
    self.assert_( result['OK'], "addFile failed when adding new file %s" % result )


    # Re-adding the same file
    result = self.dfc.addFile( { testFile: { 'PFN': 'testfilePFN',
                                         'SE': 'testSE' ,
                                         'Size':123,
                                         'GUID':1000,
                                         'Checksum':'0' } } )
    self.assert_( result["OK"], "addFile failed when adding existing file %s" % result )
    self.assert_( testFile in result["Value"]["Failed"], "addFile failed: it should not be possible to add an existing lfn %s" % result )

    ##################################################################################
    # Setting existing status of existing file
    result = self.dfc.setFileStatus( {testFile:"AprioriGood"} )
    self.assert_( result["OK"], "setFileStatus failed when setting existing status of existing file %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "setFileStatus failed: %s should be in successful (%s)" % ( testFile, result ) )

    # Setting unexisting status of existing file
    result = self.dfc.setFileStatus( {testFile:"Happy"} )
    self.assert_( result["OK"], "setFileStatus failed when setting un-existing status of existing file %s" % result )
    self.assert_( testFile in result["Value"]["Failed"], "setFileStatus should have failed %s" % result )

    # Setting existing status of unexisting file
    result = self.dfc.setFileStatus( {nonExistingFile:"Trash"} )
    self.assert_( result["OK"], "setFileStatus failed when setting existing status of non-existing file %s" % result )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "setFileStatus failed: %s should be in failed (%s)" % ( nonExistingFile, result ) )

    ##################################################################################

    result = self.dfc.isFile( [testFile, nonExistingFile] )
    self.assert_( result["OK"], "isFile failed: %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "isFile : %s should be in Successful %s" % ( testFile, result ) )
    self.assert_( result["Value"]["Successful"][testFile], "isFile : %s should be seen as a file %s" % ( testFile, result ) )
    self.assert_( nonExistingFile in result["Value"]["Successful"], "isFile : %s should be in Successful %s" % ( nonExistingFile, result ) )
    self.assert_( result["Value"]["Successful"][nonExistingFile] == False, "isFile : %s should be seen as a file %s" % ( nonExistingFile, result ) )

    result = self.dfc.changePathOwner( {testFile :  "toto", nonExistingFile : "tata"} )
    self.assert_( result["OK"], "changePathOwner failed: %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "changePathOwner : %s should be in Successful %s" % ( testFile, result ) )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "changePathOwner : %s should be in Failed %s" % ( nonExistingFile, result ) )

    result = self.dfc.changePathGroup( {testFile : "toto", nonExistingFile :"tata"} )
    self.assert_( result["OK"], "changePathGroup failed: %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "changePathGroup : %s should be in Successful %s" % ( testFile, result ) )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "changePathGroup : %s should be in Failed %s" % ( nonExistingFile, result ) )

    result = self.dfc.changePathMode( {testFile : 044, nonExistingFile : 044} )
    self.assert_( result["OK"], "changePathMode failed: %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "changePathMode : %s should be in Successful %s" % ( testFile, result ) )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "changePathMode : %s should be in Failed %s" % ( nonExistingFile, result ) )

    result = self.dfc.getFileSize( [testFile, nonExistingFile] )
    self.assert_( result["OK"], "getFileSize failed: %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "getFileSize : %s should be in Successful %s" % ( testFile, result ) )
    self.assertEqual( result["Value"]["Successful"][testFile], 123, "getFileSize got incorrect file size %s" % result )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "getFileSize : %s should be in Failed %s" % ( nonExistingFile, result ) )

    result = self.dfc.getFileMetadata( [testFile, nonExistingFile] )
    self.assert_( result["OK"], "getFileMetadata failed: %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "getFileMetadata : %s should be in Successful %s" % ( testFile, result ) )
    self.assertEqual( result["Value"]["Successful"][testFile]["Owner"], "toto", "getFileMetadata got incorrect Owner %s" % result )
    self.assertEqual( result["Value"]["Successful"][testFile]["Status"], "AprioriGood", "getFileMetadata got incorrect status %s" % result )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "getFileMetadata : %s should be in Failed %s" % ( nonExistingFile, result ) )


    result = self.dfc.removeFile( [testFile, nonExistingFile] )
    self.assert_( result["OK"], "removeFile failed: %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "removeFile : %s should be in Successful %s" % ( testFile, result ) )
    self.assert_( result["Value"]["Successful"][testFile], "removeFile : %s should be in True %s" % ( testFile, result ) )
    self.assert_( result["Value"]["Successful"][nonExistingFile], "removeFile : %s should be in True %s" % ( nonExistingFile, result ) )



class ReplicaCase( DFCTestCase ):

  def test_replicaOperations( self ):
    """
      this test requires the SE to be properly defined in the CS -> NO IT DOES NOT!!
    """
    # Adding a new file
    result = self.dfc.addFile( { testFile: { 'PFN': 'testfile',
                                         'SE': 'testSE' ,
                                         'Size':123,
                                         'GUID':1000,
                                         'Checksum':'0' } } )
    self.assert_( result['OK'], "addFile failed when adding new file %s" % result )

    # Adding new replica
    result = self.dfc.addReplica( {testFile : {"PFN" : "testFilePFN", "SE" : "otherSE"}} )
    self.assert_( result['OK'], "addReplica failed when adding new Replica %s" % result )
    self.assert_( testFile in result['Value']["Successful"], "addReplica failed when adding new Replica %s" % result )

    # Adding the same replica
    result = self.dfc.addReplica( {testFile : {"PFN" : "testFilePFN", "SE" : "otherSE"}} )
    self.assert_( result['OK'], "addReplica failed when adding new Replica %s" % result )
    self.assert_( testFile in result['Value']["Successful"], "addReplica failed when adding new Replica %s" % result )

    # Adding replica of a non existing file
    result = self.dfc.addReplica( {nonExistingFile : {"PFN" : "IdontexistPFN", "SE" : "otherSE"}} )
    self.assert_( result['OK'], "addReplica failed when adding Replica to non existing Replica %s" % result )
    self.assert_( nonExistingFile in result['Value']["Failed"], "addReplica for non existing file should go in Failed  %s" % result )


    # Setting existing status of existing Replica
    result = self.dfc.setReplicaStatus( {testFile: {"Status" : "Trash", "SE" : "otherSE"}} )
    self.assert_( result["OK"], "setReplicaStatus failed when setting existing status of existing Replica %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "setReplicaStatus failed: %s should be in successful (%s)" % ( testFile, result ) )

    # Setting non existing status of existing Replica
    result = self.dfc.setReplicaStatus( {testFile: {"Status" : "randomStatus", "SE" : "otherSE"}} )
    self.assert_( result["OK"], "setReplicaStatus failed when setting non-existing status of existing Replica %s" % result )
    self.assert_( testFile in result["Value"]["Failed"], "setReplicaStatus failed: %s should be in Failed (%s)" % ( testFile, result ) )

    # Setting existing status of non-existing Replica
    result = self.dfc.setReplicaStatus( {testFile: {"Status" : "Trash", "SE" : "nonExistingSe"}} )
    self.assert_( result["OK"], "setReplicaStatus failed when setting existing status of non-existing Replica %s" % result )
    self.assert_( testFile in result["Value"]["Failed"], "setReplicaStatus failed: %s should be in Failed (%s)" % ( testFile, result ) )

    # Setting existing status of non-existing File
    result = self.dfc.setReplicaStatus( {nonExistingFile: {"Status" : "Trash", "SE" : "nonExistingSe"}} )
    self.assert_( result["OK"], "setReplicaStatus failed when setting existing status of non-existing File %s" % result )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "setReplicaStatus failed: %s should be in Failed (%s)" % ( nonExistingFile, result ) )


    # Getting existing status of existing Replica but not visible
    result = self.dfc.getReplicaStatus( {testFile: "testSE"} )
    self.assert_( result["OK"], "getReplicaStatus failed when getting existing status of existing Replica %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "getReplicaStatus failed: %s should be in Successful (%s)" % ( testFile, result ) )

    # Getting existing status of existing Replica but not visible
    result = self.dfc.getReplicaStatus( {testFile : "otherSE"} )
    self.assert_( result["OK"], "getReplicaStatus failed when getting existing status of existing Replica but not visible %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "getReplicaStatus failed: %s should be in Successful (%s)" % ( testFile, result ) )

    # Getting status of non-existing File but not visible
    result = self.dfc.getReplicaStatus( {nonExistingFile: "testSE"} )
    self.assert_( result["OK"], "getReplicaStatus failed when getting status of non existing File %s" % result )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "getReplicaStatus failed: %s should be in failed (%s)" % ( nonExistingFile, result ) )

    # Getting replicas of existing File and non existing file, seeing all replicas
    result = self.dfc.getReplicas( [testFile, nonExistingFile], allStatus = True )
    self.assert_( result["OK"], "getReplicas failed %s" % result )
    self.assert_( testFile in result["Value"]["Successful"], "getReplicas failed, %s should be in Successful %s" % ( testFile, result ) )
    self.assertEqual( result["Value"]["Successful"][testFile], {"otherSE" : testFile, "testSE" : testFile}, "getReplicas failed, %s should be in Successful %s" % ( testFile, result ) )
    self.assert_( nonExistingFile in result["Value"]["Failed"], "getReplicas failed, %s should be in Failed %s" % ( nonExistingFile, result ) )


    expectedSize = {'PhysicalSize': {'TotalSize': 246,
                                      'otherSE': {'Files': 1, 'Size': 123},
                                       'TotalFiles': 2,
                                       'testSE': {'Files': 1, 'Size': 123}},
                                 'LogicalFiles': 1, 'LogicalDirectories': 0L, 'LogicalSize': 123}

    result = self.dfc.getDirectorySize( [testDir], True, False )
    self.assert_( result["OK"], "getDirectorySize failed: %s" % result )
    self.assert_( testDir in result["Value"]["Successful"], "getDirectorySize : %s should be in Successful %s" % ( testDir, result ) )
    self.assertEqual( result["Value"]["Successful"][testDir], expectedSize, "getDirectorySize got incorrect directory size %s" % result )

    result = self.dfc.getDirectorySize( [testDir], True, True )

    self.assert_( result["OK"], "getDirectorySize (calc) failed: %s" % result )
    self.assert_( testDir in result["Value"]["Successful"], "getDirectorySize (calc): %s should be in Successful %s" % ( testDir, result ) )
    self.assertEqual( result["Value"]["Successful"][testDir], expectedSize, "getDirectorySize got incorrect directory size %s" % result )



    # removing master replica
    result = self.dfc.removeReplica( {testFile : { "SE" : "testSE"}} )
    self.assert_( result['OK'], "removeReplica failed when removing master Replica %s" % result )
    self.assert_( testFile in result['Value']["Successful"], "removeReplica failed when removing master Replica %s" % result )

    # removing non existing replica of existing File
    result = self.dfc.removeReplica( {testFile : { "SE" : "nonExistingSe2"}} )
    self.assert_( result['OK'], "removeReplica failed when removing non existing Replica %s" % result )
    self.assert_( testFile in result['Value']["Successful"], "removeReplica failed when removing new Replica %s" % result )

    # removing non existing replica of non existing file
    result = self.dfc.removeReplica( {nonExistingFile : { "SE" : "nonExistingSe3"}} )
    self.assert_( result['OK'], "removeReplica failed when removing replica of non existing File %s" % result )
    self.assert_( nonExistingFile in result['Value']["Successful"], "removeReplica of non existing file, %s should be in Successful %s" % ( nonExistingFile, result ) )

    # removing last replica
    result = self.dfc.removeReplica( {testFile : { "SE" : "otherSE"}} )
    self.assert_( result['OK'], "removeReplica failed when removing last Replica %s" % result )
    self.assert_( testFile in result['Value']["Successful"], "removeReplica failed when removing last Replica %s" % result )

    # Cleaning after us
    result = self.dfc.removeFile( testFile )
    self.assert_( result["OK"], "removeFile failed: %s" % result )



class DirectoryCase( DFCTestCase ):

  def test_directoryOperations( self ):
    """
      Tests the Directory related Operations
      this test requires the SE to be properly defined in the CS -> NO IT DOES NOT!!
    """
    # Adding a new directory
    result = self.dfc.createDirectory( testDir )
    self.assert_( result['OK'], "addDirectory failed when adding new directory %s" % result )

    result = self.dfc.addFile( { testFile: { 'PFN': 'testfile',
                                         'SE': 'testSE' ,
                                         'Size':123,
                                         'GUID':1000,
                                         'Checksum':'0' } } )
    self.assert_( result['OK'], "addFile failed when adding new file %s" % result )



    # Re-adding the same directory (CAUTION, different from addFile)
    result = self.dfc.createDirectory( testDir )
    self.assert_( result["OK"], "addDirectory failed when adding existing directory %s" % result )
    self.assert_( testDir in result["Value"]["Successful"], "addDirectory failed: it should be possible to add an existing lfn %s" % result )


    result = self.dfc.isDirectory( [testDir, nonExistingDir] )
    self.assert_( result["OK"], "isDirectory failed: %s" % result )
    self.assert_( testDir in result["Value"]["Successful"], "isDirectory : %s should be in Successful %s" % ( testDir, result ) )
    self.assert_( result["Value"]["Successful"][testDir], "isDirectory : %s should be seen as a directory %s" % ( testDir, result ) )
    self.assert_( nonExistingDir in result["Value"]["Successful"], "isDirectory : %s should be in Successful %s" % ( nonExistingDir, result ) )
    self.assert_( result["Value"]["Successful"][nonExistingDir] == False, "isDirectory : %s should be seen as a directory %s" % ( nonExistingDir, result ) )

    result = self.dfc.getDirectorySize( [testDir, nonExistingDir], False, False )
    self.assert_( result["OK"], "getDirectorySize failed: %s" % result )
    self.assert_( testDir in result["Value"]["Successful"], "getDirectorySize : %s should be in Successful %s" % ( testDir, result ) )
    self.assertEqual( result["Value"]["Successful"][testDir], {'LogicalFiles': 1, 'LogicalDirectories': 0, 'LogicalSize': 123}, "getDirectorySize got incorrect directory size %s" % result )
    self.assert_( nonExistingDir in result["Value"]["Failed"], "getDirectorySize : %s should be in Failed %s" % ( nonExistingDir, result ) )


    result = self.dfc.getDirectorySize( [testDir, nonExistingDir], False, True )
    self.assert_( result["OK"], "getDirectorySize (calc) failed: %s" % result )
    self.assert_( testDir in result["Value"]["Successful"], "getDirectorySize (calc): %s should be in Successful %s" % ( testDir, result ) )
    self.assertEqual( result["Value"]["Successful"][testDir], {'LogicalFiles': 1, 'LogicalDirectories': 0, 'LogicalSize': 123}, "getDirectorySize got incorrect directory size %s" % result )
    self.assert_( nonExistingDir in result["Value"]["Failed"], "getDirectorySize (calc) : %s should be in Failed %s" % ( nonExistingDir, result ) )



    result = self.dfc.listDirectory( [parentDir, testDir, nonExistingDir] )
    self.assert_( result["OK"], "listDirectory failed: %s" % result )
    self.assert_( parentDir in result["Value"]["Successful"], "listDirectory : %s should be in Successful %s" % ( parentDir, result ) )
    self.assertEqual( result["Value"]["Successful"][parentDir]["SubDirs"].keys(), [testDir], \
                     "listDir : incorrect content for %s (%s)" % ( parentDir, result ) )
    self.assert_( testDir in result["Value"]["Successful"], "listDirectory : %s should be in Successful %s" % ( testDir, result ) )
    self.assertEqual( result["Value"]["Successful"][testDir]["Files"].keys(), [testFile], \
                     "listDir : incorrect content for %s (%s)" % ( testDir, result ) )
    self.assert_( nonExistingDir in result["Value"]["Failed"], "listDirectory : %s should be in Failed %s" % ( nonExistingDir, result ) )



    # Cleaning after us
    result = self.dfc.removeFile( testFile )
    self.assert_( result["OK"], "removeFile failed: %s" % result )

    result = self.dfc.removeDirectory( [testDir, nonExistingDir] )
    self.assert_( result["OK"], "removeDirectory failed: %s" % result )
    self.assert_( testDir in result["Value"]["Successful"], "removeDirectory : %s should be in Successful %s" % ( testDir, result ) )
    self.assert_( result["Value"]["Successful"][testDir], "removeDirectory : %s should be in True %s" % ( testDir, result ) )
    self.assert_( nonExistingDir in result["Value"]["Successful"], "removeDirectory : %s should be in Successful %s" % ( nonExistingDir, result ) )
    self.assert_( result["Value"]["Successful"][nonExistingDir], "removeDirectory : %s should be in True %s" % ( nonExistingDir, result ) )



if __name__ == '__main__':


  suite = unittest.defaultTestLoader.loadTestsFromTestCase( UserGroupCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( FileCase ) )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( ReplicaCase ) )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( DirectoryCase ) )

  testResult = unittest.TextTestRunner( verbosity = 2 ).run( suite )

