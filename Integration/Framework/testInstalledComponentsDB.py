"""
Tests the ComponentMonitoring DB and Service by creating, checking,
updating and removing several instances of each table in the DB
This program assumes that the service Framework/ComponentMonitoring is running
"""

import datetime
from DIRAC.FrameworkSystem.Client.ComponentMonitoringClient \
      import ComponentMonitoringClient
from DIRAC import gLogger, S_OK, S_ERROR

class ComponentMonitoringTest():
  """
  Contains methods for testing of separate elements
  """

  def __init__( self ):
    self.client = ComponentMonitoringClient()

  def testComponents( self ):
    """
    Test the Components database operations
    """

    results = []

    # Create a sample component
    result = self.client.addComponent( { 'System': 'Test',
                                          'Module': 'TestModule',
                                          'Type': 'TestingFeature' } )
    if result[ 'OK' ]:
      result = S_OK( 'Creation of complete Component: Component was created' )
    else:
      result = S_ERROR \
              ( 'Creation of complete Component: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the component exists
    result = self.client.getComponents( { 'System': 'Test',
                                          'Module': 'TestModule',
                                          'Type': 'TestingFeature' },
                                          False,
                                          False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_OK( 'Checking existence of Component: Component exists' )
      else:
        result = S_ERROR \
            ( 'Checking existence of Component: Could not find the component' )
    else:
      result = S_ERROR( 'Checking existence of Component: %s' %
                          ( result[ 'Message' ] ) )
    results.append( result )

    # Update the fields of the created component
    result = self.client.updateComponents( { 'System': 'Test',
                                              'Module': 'TestModule',
                                              'Type': 'TestingFeature' },
                                            { 'Module': 'NewTestModule' } )
    if result[ 'OK' ]:
      result = S_OK( 'Updating Component: Component updated' )
    else:
      result = S_ERROR( 'Updating Component: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the component with the modified fields exists
    result = self.client.getComponents( { 'System': 'Test',
                                          'Module': 'NewTestModule',
                                          'Type': 'TestingFeature' },
                                          False,
                                          False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_OK \
                ( 'Checking existence of updated Component: Component exists' )
      else:
        result = S_ERROR( 'Checking existence of updated Component: ' \
                          'Could not find the component' )
    else:
      result = S_ERROR( 'Checking existence of updated Component: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Remove the Component
    result = self.client.removeComponents( { 'System': 'Test',
                                              'Module': 'NewTestModule',
                                              'Type': 'TestingFeature' } )
    if result[ 'OK' ]:
      result = S_OK( 'Removing Component: Component removed' )
    else:
      result = S_ERROR( 'Removing Component: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the component was actually removed
    result = self.client.getComponents( { 'System': 'Test',
                                          'Module': 'NewTestModule',
                                          'Type': 'TestingFeature' },
                                          False,
                                          False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_ERROR \
                ( 'Checking existence of removed Component: Component exists' )
      else:
        result = S_OK( 'Checking existence of removed Component: ' \
                                                'Could not find the component' )
    else:
      result = S_ERROR( 'Checking existence of updated Component: %s' %
                                                       ( result[ 'Message' ] ) )
    results.append( result )

    # Try to create an incomplete component
    result = self.client.addComponent( { 'System': 'Test' } )
    if result[ 'OK' ]:
      result = S_ERROR \
                  ( 'Creation of incomplete Component: Component was created' )
    else:
      result = S_OK \
              ( 'Creation of incomplete Component: Component was not created' )
    results.append( result )

    # Multiple removal
    self.client.addComponent( { 'System': 'Test',
                                'Module': 'TestModule1',
                                'Type': 'TestingFeature1' } )
    self.client.addComponent( { 'System': 'Test',
                                'Module': 'TestModule2',
                                'Type': 'TestingFeature1' } )
    self.client.addComponent( { 'System': 'Test',
                                'Module': 'TestModule1',
                                'Type': 'TestingFeature2' } )

    self.client.removeComponents \
                              ( { 'System': 'Test', 'Module': 'TestModule1' } )

    result = self.client.getComponents( { 'System': 'Test',
                                          'Module': 'TestModule2',
                                          'Type': 'TestingFeature1' },
                                          False,
                                          False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) < 1:
        result = S_ERROR( 'Multiple removal: Could not find the Component ' \
                                                        'that was not removed' )

    result = self.client.getComponents( { 'System': 'Test',
                                          'Module': 'TestModule1' },
                                          False,
                                          False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_ERROR \
                      ( 'Multiple removal: Found a Component that was removed' )

    self.client.removeComponents( { 'System': 'Test',
                                    'Module': 'TestModule2',
                                    'Type': 'TestingFeature1' } )

    if result[ 'OK' ]:
      result = S_OK \
              ( 'Multiple removal: Only the specified Components were removed' )
    results.append( result )

    return results

  def testHosts( self ):
    """
    Tests the Hosts database operations
    """

    results = []

    # Create a sample host
    result = self.client.addHost( { 'HostName': 'TestHost', 'CPU': 'TestCPU' } )
    if result[ 'OK' ]:
      result = S_OK( 'Creation of complete Host: Host was created' )
    else:
      result = S_ERROR( 'Creation of complete Host: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the host exists
    result = self.client.getHosts( { 'HostName': 'TestHost',
                                      'CPU': 'TestCPU' },
                                      False,
                                      False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_OK( 'Checking existence of Host: Host exists' )
      else:
        result = S_ERROR \
                      ( 'Checking existence of Host: Could not find the host' )
    else:
      result = S_ERROR( 'Checking existence of Host: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Update the fields of the created host
    result = self.client.updateHosts( { 'HostName': 'TestHost',
                                        'CPU': 'TestCPU' },
                                      { 'HostName': 'StillATestHost' } )
    if result[ 'OK' ]:
      result = S_OK( 'Updating Host: Host updated' )
    else:
      result = S_ERROR( 'Updating Host: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the host with the modified fields exists
    result = self.client.getHosts( { 'HostName': 'StillATestHost',
                                      'CPU': 'TestCPU' },
                                      False,
                                      False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_OK( 'Checking existence of updated Host: Host exists' )
      else:
        result = S_ERROR( 'Checking existence of updated Host: ' \
                                                    'Could not find the host' )
    else:
      result = S_ERROR( 'Checking existence of updated Host: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Remove the Host
    result = self.client.removeHosts( { 'HostName': 'StillATestHost',
                                        'CPU': 'TestCPU' } )
    if result[ 'OK' ]:
      result = S_OK( 'Removing Host: Host removed' )
    else:
      result = S_ERROR( 'Removing Host: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the host was actually removed
    result = self.client.getHosts( { 'HostName': 'StillATestHost',
                                      'CPU': 'TestCPU' },
                                      False,
                                      False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_ERROR( 'Checking existence of removed Host: Host exists' )
      else:
        result = S_OK( 'Checking existence of removed Host: ' \
                                                    'Could not find the host' )
    else:
      result = S_ERROR( 'Checking existence of updated Host: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Try to create an incomplete host
    result = self.client.addHost( { 'HostName': 'TestHost' } )
    if result[ 'OK' ]:
      result = S_ERROR( 'Creation of incomplete Host: Host was created' )
    else:
      result = S_OK( 'Creation of incomplete Host: Host was not created' )
    results.append( result )

    # Multiple removal
    self.client.addHost( { 'HostName': 'TestHost', 'CPU': 'TestCPU1' } )
    self.client.addHost( { 'HostName': 'TestHost', 'CPU': 'TestCPU2' } )
    self.client.addHost( { 'HostName': 'TestHost', 'CPU': 'TestCPU1' } )

    self.client.removeHosts( { 'CPU': 'TestCPU1' } )

    result = self.client.getHosts( { 'HostName': 'TestHost',
                                      'CPU': 'TestCPU2' },
                                      False,
                                      False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) < 1:
        result = S_ERROR \
            ( 'Multiple removal: Could not find the Host that was not removed' )

    result = self.client.getHosts( { 'HostName': 'TestHost',
                                      'CPU': 'TestCPU1' },
                                      False,
                                      False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_ERROR( 'Multiple removal: Found a Host that was removed' )

    self.client.removeHosts( { 'HostName': 'TestHost', 'CPU': 'TestCPU2' } )

    if result[ 'OK' ]:
      result = S_OK( 'Multiple removal: Only the specified Hosts were removed' )
    results.append( result )

    return results

  def testInstallations( self ):
    """
    Test the InstalledComponents database operations
    """

    results = []

    # Create a sample installation
    result = self.client.addInstallation \
                              ( { 'InstallationTime': datetime.datetime.now(),
                                  'UnInstallationTime': datetime.datetime.now(),
                                  'Instance': 'TestInstallA111' },
                                  { 'System': 'UnexistentSystem',
                                    'Module': 'UnexistentModule',
                                    'Type': 'UnexistentType' },
                                  { 'HostName': 'fictional',
                                    'CPU': 'TestCPU' },
                                  True )
    if result[ 'OK' ]:
      result = S_OK \
              ( 'Creation of complete Installation: Installation was created' )
    else:
      result = S_ERROR( 'Creation of complete Installation: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the installation exists
    result = self.client.getInstallations( { 'Instance': 'TestInstallA111' },
                                           { 'System': 'UnexistentSystem',
                                              'Module': 'UnexistentModule',
                                              'Type': 'UnexistentType' },
                                            { 'HostName': 'fictional',
                                              'CPU': 'TestCPU' },
                                            False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_OK \
                  ( 'Checking existence of Installation: Installation exists' )
      else:
        result = S_ERROR( 'Checking existence of Installation: ' \
                                            'Could not find the installation' )
    else:
      result = S_ERROR( 'Checking existence of Installation: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Update the fields of the created installation
    result = self.client.updateInstallations( { 'Instance': 'TestInstallA111' },
                                              { 'System': 'UnexistentSystem',
                                                'Module': 'UnexistentModule',
                                                'Type': 'UnexistentType' },
                                              { 'HostName': 'fictional',
                                                'CPU': 'TestCPU' },
                                              { 'Instance': 'TestInstallA222' }
                                            )
    if result[ 'OK' ]:
      result = S_OK( 'Updating Installation: Installation updated' )
    else:
      result = S_ERROR( 'Updating Installation: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the installation with the modified fields exists
    result = self.client.getInstallations( { 'Instance': 'TestInstallA222' },
                                           { 'System': 'UnexistentSystem',
                                              'Module': 'UnexistentModule',
                                              'Type': 'UnexistentType' },
                                            { 'HostName': 'fictional',
                                              'CPU': 'TestCPU' },
                                            False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_OK( 'Checking existence of updated Installation: ' \
                                                        'Installation exists' )
      else:
        result = S_ERROR( 'Checking existence of updated Installation: ' \
                                            'Could not find the installation' )
    else:
      result = S_ERROR( 'Checking existence of updated Installation: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Remove the Installation
    result = self.client.removeInstallations( { 'Instance': 'TestInstallA222' },
                                              { 'System': 'UnexistentSystem',
                                                'Module': 'UnexistentModule',
                                                'Type': 'UnexistentType' },
                                              { 'HostName': 'fictional',
                                                'CPU': 'TestCPU' } )
    if result[ 'OK' ]:
      result = S_OK( 'Removing Installation: Installation removed' )
    else:
      result = S_ERROR( 'Removing Installation: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    # Check if the installation was actually removed
    result = self.client.getInstallations( { 'Instance': 'TestInstallA222' },
                                            { 'System': 'UnexistentSystem',
                                              'Module': 'UnexistentModule',
                                              'Type': 'UnexistentType' },
                                            { 'HostName': 'fictional',
                                              'CPU': 'TestCPU' },
                                            False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_ERROR( 'Checking existence of removed Installation: ' \
                                                        'Installation exists' )
      else:
        result = S_OK( 'Checking existence of removed Installation: ' \
                                            'Could not find the installation' )
    else:
      result = S_ERROR( 'Checking existence of updated Installation: %s' %
                                                      ( result[ 'Message' ] ) )
    results.append( result )

    # Create an installation associated with nonexistent Component
    result = self.client.addInstallation( 
                                { 'InstallationTime': datetime.datetime.now(),
                                  'UnInstallationTime': datetime.datetime.now(),
                                  'Instance': 'TestInstallA333' },
                                { 'System': 'UnexistentSystem',
                                  'Module': 'UnexistentModule22A',
                                  'Type': 'UnexistentType' },
                                { 'HostName': 'fictional',
                                  'CPU': 'TestCPU' } ,
                                False )
    if not result[ 'OK' ]:
      result = S_OK( 'Creation of incomplete Installation: ' \
                                                'Installation was not created' )
    else:
      result = S_ERROR( 'Creation of incomplete Installation: ' \
                                                    'Installation was created' )
    results.append( result )

    # Multiple removal
    self.client.addInstallation( 
                                { 'InstallationTime': datetime.datetime.now(),
                                  'UnInstallationTime': datetime.datetime.now(),
                                  'Instance': 'MultipleRemovalInstall1' },
                                { 'System': 'UnexistentSystem',
                                  'Module': 'UnexistentModule',
                                  'Type': 'UnexistentType' },
                                { 'HostName': 'fictional',
                                  'CPU': 'TestCPU' },
                                False )
    self.client.addInstallation( 
                                { 'InstallationTime': datetime.datetime.now(),
                                  'UnInstallationTime': datetime.datetime.now(),
                                  'Instance': 'MultipleRemovalInstall2' },
                                { 'System': 'UnexistentSystem',
                                  'Module': 'UnexistentModule',
                                  'Type': 'UnexistentType' },
                                { 'HostName': 'fictional',
                                  'CPU': 'TestCPU' } ,
                                False )
    self.client.addInstallation( 
                                { 'InstallationTime': datetime.datetime.now(),
                                  'UnInstallationTime': datetime.datetime.now(),
                                  'Instance': 'MultipleRemovalInstall3' },
                                { 'System': 'UnexistentSystem',
                                  'Module': 'UnexistentModule2',
                                  'Type': 'UnexistentType' },
                                { 'HostName': 'fictional',
                                  'CPU': 'TestCPU' },
                                True )

    result = self.client.getInstallations( 
                  { 'Instance':
                    [ 'MultipleRemovalInstall1', 'MultipleRemovalInstall3' ] },
                  {},
                  {},
                  False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) != 2:
        result = S_ERROR( 'Checking selection with IN: ' \
                                  'Incorrect number of installations returned' )
      else:
        result = S_OK( 'Checking selection with IN: ' \
                                    'Correct number of installations returned' )
    else:
      result = S_ERROR \
                  ( 'Checking selection with IN: %s' % ( result[ 'Message' ] ) )
    results.append( result )

    self.client.removeInstallations( {},
                                     { 'Module': 'UnexistentModule' },
                                     {} )

    result = self.client.getInstallations( {},
                                      { 'Module': 'UnexistentModule2' },
                    {}, False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) < 1:
        result = S_ERROR( 'Multiple removal: ' \
                        'Could not find the Installation that was not removed' )

    result = self.client.getInstallations( {},
                                           { 'Module': 'UnexistentModule' },
                                           {},
                                           False )
    if result[ 'OK' ]:
      if len( result[ 'Value' ] ) > 0:
        result = S_ERROR \
                  ( 'Multiple removal: Found an Installation that was removed' )

    self.client.removeInstallations( {},
                                     { 'Module': 'UnexistentModule2' },
                                     {} )

    if result[ 'OK' ]:
      result = S_OK \
          ( 'Multiple removal: Only the specified Installations were removed' )
    results.append( result )

    # Clean up what we created
    self.client.removeHosts( { 'HostName': 'fictional', 'CPU': 'TestCPU' } )
    self.client.removeComponents( { 'System': 'UnexistentSystem',
                                    'Module': 'UnexistentModule',
                                    'Type': 'UnexistentType' } )
    self.client.removeComponents( { 'System': 'UnexistentSystem',
                                    'Module': 'UnexistentModule2',
                                    'Type': 'UnexistentType' } )

    return results

  def runTests( self ):
    """
    Runs the test for all the databases in succession
    """

    gLogger.notice( 'Testing Component ...' )
    testResults = self.testComponents()
    for testResult in testResults:
      if not testResult[ 'OK' ]:
        gLogger.notice( 'FAILED: %s' % ( testResult[ 'Message' ] ) )
      else:
        gLogger.notice( 'SUCCESS: %s' % ( testResult[ 'Value' ] ) )
    gLogger.notice( 'Testing Host ...' )
    testResults = self.testHosts()
    for testResult in testResults:
      if not testResult[ 'OK' ]:
        gLogger.notice( 'FAILED: %s' % ( testResult[ 'Message' ] ) )
      else:
        gLogger.notice( 'SUCCESS: %s' % ( testResult[ 'Value' ] ) )
    gLogger.notice( 'Testing InstalledComponent ...' )
    testResults = self.testInstallations()
    for testResult in testResults:
      if not testResult[ 'OK' ]:
        gLogger.notice( 'FAILED: %s' % ( testResult[ 'Message' ] ) )
      else:
        gLogger.notice( 'SUCCESS: %s' % ( testResult[ 'Value' ] ) )

try:
  test = ComponentMonitoringTest()
  test.runTests()
except Exception, e:
  gLogger.error( e )
