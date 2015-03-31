""" This is a test of the chain
    PilotAgentsClientClient -> PilotAgentsHandler -> PilotAgentsDB

    It supposes that the DB is present, and that the service is running
"""

import unittest
from DIRAC.WorkloadManagementSystem.Client.PilotAgentsClient import PilotAgentsClient

class TestPilotAgents( unittest.TestCase ):
  
  def setUp( self ):
    self.pilotsLoggingClient = PilotAgentsClient()
    
  def tearDown( self ):
    pass
  
class PilotsLogging( TestPilotAgents ):
  
  def test_PilotsLogging(self):
    
    resp = self.pilotsLoggingClient.addPilotsLogging('11111111-1111-1111-1111-111111111111', 'status1', 'minorStatus1', 1427721819.0, 'test', 0)
    self.assert_(resp['OK'], 'Failed to add PilotsLogging')
    resp = self.pilotsLoggingClient.setPilotsUUIDtoIDMapping('11111111-1111-1111-1111-111111111111', 1)
    self.assert_(resp['OK'], 'Failed to add PilotsUUIDtoIDMapping')
    resp = self.pilotsLoggingClient.getPilotsLogging(1)
    self.assert_(resp['OK'], 'Failed to get PilotsLogging')
    test_sample = {
                   'PilotUUID': '11111111-1111-1111-1111-111111111111',
                   'PilotID': 1,
                   'Status': 'status1',
                   'MinorStatus': 'minorStatus1',
                   'TimeStamp': 1427721819.0,
                   'Source': 'test'
                   }
    self.assertEqual(resp['Value'], [ test_sample ], 'Wrong data comes out of Service')
    resp = self.pilotsLoggingClient.deletePilotsLogging(1)
    self.assert_(resp['OK'], 'Failed to delete PilotsLogging')
    resp = self.pilotsLoggingClient.getPilotsLogging(1)
    self.assert_(resp['OK'], 'Failed to get PilotsLogging')
    self.assertEqual(resp['Value'], [], 'PilotsLogging was not really deleted')
    
if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( TestPilotAgents )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( PilotsLogging ) )
  testResult = unittest.TextTestRunner( verbosity = 2 ).run( suite )
  