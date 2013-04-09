""" Testing the API and a bit more.
    It will submit a number of test jobs locally (via runLocal), using the python unittest to assess the results.
    Can be automatized.
"""

from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()

import os.path
import unittest

from TestDIRAC.Utils.Utils import cleanTestDir

from DIRAC import gLogger
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac

gLogger.setLevel( 'DEBUG' )

cwd = os.path.realpath( '.' )

class UserJobTestCase( unittest.TestCase ):
  """ Base class for the UserJob test cases
  """
  def setUp( self ):
    cleanTestDir()

    gLogger.setLevel( 'DEBUG' )
    self.dirac = Dirac()


class HelloWorldSuccess( UserJobTestCase ):
  """ Simplest ever. helloWorld.py just calls 'echo'
  """
  def test_execute( self ):

    job = Job()

    job.setName( "helloWorld-test" )
    job.setExecutable( "helloWorld.py" )
    res = job.runLocal( self.dirac )
    self.assertTrue( res['OK'] )

class HelloWorldPlusSuccess( UserJobTestCase ):
  """ Adding quite a lot of calls from the API, for pure test purpose
  """

  def test_execute( self ):

    job = Job()

    job.setName( "helloWorld-test" )
    job.setExecutable( "helloWorld.py", arguments = "This is an argument", logFile = "aLogFileForTest.txt" )
    job.setBannedSites( ['LCG.SiteA.com', 'DIRAC.SiteB.org'] )
    job.setOwner( 'ownerName' )
    job.setOwnerGroup( 'ownerGroup' )
    job.setName( 'jobName' )
    job.setJobGroup( 'jobGroup' )
    job.setType( 'jobType' )
    job.setDestination( 'DIRAC.someSite.ch' )
    job.setCPUTime( 12345 )
    job.setLogLevel( 'DEBUG' )

    res = job.runLocal( self.dirac )
    self.assertTrue( res['OK'] )


# class CatSuccess( UserJobTestCase ):
#  def test_execute( self ):
#
#    job = Job()
#
#    job.setName( "cat-test" )
#    job.setExecutable( "cat.py" )
#    job.set
#    res = job.runLocal( self.dirac )
#    self.assertTrue( res['OK'] )


if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( UserJobTestCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( HelloWorldSuccess ) )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( HelloWorldPlusSuccess ) )
  testResult = unittest.TextTestRunner( verbosity = 2 ).run( suite )

