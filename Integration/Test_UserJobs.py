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
  ''' Base class for the UserJob test cases
  '''
  def setUp( self ):
    cleanTestDir()

    gLogger.setLevel( 'DEBUG' )
    self.dirac = Dirac()


class HelloWorldSuccess( UserJobTestCase ):
  def test_execute( self ):

    job = Job()

    job.setName( "helloWorld-test" )
    job.setExecutable( "exe-script.py" )
    res = job.runLocal( self.dirac )
    self.assertTrue( res['OK'] )

if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( UserJobTestCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( HelloWorldSuccess ) )
  testResult = unittest.TextTestRunner( verbosity = 2 ).run( suite )

