""" This is a test of the chain
    WMSClient -> JobManager & SandboxStore -> JobDB & SandboxMetadataDB
    
    It supposes that the DBs are present, and that the services are running
"""

import unittest  # , importlib
import os, tempfile
# from mock import Mock

from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()

from DIRAC.Interfaces.API.Job import Job
from DIRAC.WorkloadManagementSystem.Client.WMSClient import WMSClient



def helloWorldJob():
  job = Job()
  job.setName( "helloWorld" )
  job.setInputSandbox( '../../Integration/exe-script.py' )
  job.setExecutable( "exe-script.py", "", "helloWorld.log" )
  return job

def createFile( job ):
  tmpdir = tempfile.mkdtemp()
  jobDescription = tmpdir + '/jobDescription.xml'
  fd = os.open( jobDescription, os.O_RDWR | os.O_CREAT )
  os.write( fd, job._toXML() )
  os.close( fd )
  return jobDescription




class TestWMSTestCase( unittest.TestCase ):

  def setUp( self ):
#     self.getDIRACPlatformMock = Mock()
#     self.jobDB = importlib.import_module( 'DIRAC.WorkloadManagementSystem.DB.JobDB' )
#     self.jobDB.getDIRACPlatform = self.getDIRACPlatformMock
    pass

  def tearDown( self ):
    del self.jobDB

class WMSChain( TestWMSTestCase ):

  def test_submitJob( self ):

    # Simplest job
    job = helloWorldJob()
    jobDescription = createFile( job )

    res = WMSClient().submitJob( job._toJDL( xmlFile = jobDescription ) )
    self.assert_( res['OK'] )
    self.assertEqual( type( res['Value'] ), int )

    # Adding a platform that should not exist
    job = helloWorldJob()
    job.setPlatform( "notExistingPlatform" )

    jobDescription = createFile( job )

    res = WMSClient().submitJob( job._toJDL( xmlFile = jobDescription ) )
    self.assertFalse( res['OK'] )

    # Adding a platform
    self.getDIRACPlatformMock.return_value = {'OK': False}

    job = helloWorldJob()
    job.setPlatform( "x86_64-slc5-gcc41-opt" )

    jobDescription = createFile( job )

    res = WMSClient().submitJob( job._toJDL( xmlFile = jobDescription ) )
    self.assert_( res['OK'] )
    self.assertEqual( type( res['Value'] ), int )






#     job.setCPUTime( 17800 )
#     job.setBannedSites( ['LCG.CERN.ch', 'LCG.CNAF.it', 'LCG.GRIDKA.de', 'LCG.IN2P3.fr',
#                          'LCG.NIKHEF.nl', 'LCG.PIC.es', 'LCG.RAL.uk', 'LCG.SARA.nl'] )


if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( TestWMSTestCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( WMSChain ) )
  testResult = unittest.TextTestRunner( verbosity = 2 ).run( suite )
