#!/usr/bin/env python
""" update local cfg
"""

from DIRAC.Core.Base import Script

Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s [option|cfgFile] ... DB ...' % Script.scriptName,
                                     'Arguments:',
                                     '  setup: Name of the build setup (mandatory)'] ) )

Script.parseCommandLine()

args = Script.getPositionalArgs()

if len( args ) < 1:
  Script.showHelp()
  exit( -1 )

setupName = args[0]

import os.path

from DIRAC.Core.Utilities.CFG import CFG

localCfg = CFG()

# Which file
localConfigFile = os.path.join( '.', 'etc', 'Production.cfg' )
localCfg.loadFromFile( localConfigFile )

# Where to store outputs
if not os.path.isdir( '%s/sandboxes' % setupName ):
  os.makedirs( '%s/sandboxes' % setupName )
localCfg.setOption( 'Systems/WorkloadManagement/Production/Services/SandboxStore/BasePath',
                    '%s/sandboxes' % setupName )
localCfg.setOption( 'Systems/WorkloadManagement/Production/Services/SandboxStore/LogLevel', 'DEBUG' )

# Now setting a SandboxSE as the following:
#     ProductionSandboxSE
#     {
#       BackendType = DISET
#       AccessProtocol.1
#       {
#         Host = localhost
#         Port = 9196
#         ProtocolName = DIP
#         Protocol = dips
#         Path = /scratch/workspace/%s/sandboxes % setupName
#         Access = remote
#         SpaceToken =
#         WSUrl =
#       }
#     }
localCfg.createNewSection( 'Resources/StorageElements/' )
localCfg.createNewSection( 'Resources/StorageElements/ProductionSandboxSE' )
localCfg.setOption( 'Resources/StorageElements/ProductionSandboxSE/BackendType', 'DISET' )
localCfg.createNewSection( 'Resources/StorageElements/ProductionSandboxSE/AccessProtocol.1' )
localCfg.setOption( 'Resources/StorageElements/ProductionSandboxSE/AccessProtocol.1/Host', 'localhost' )
localCfg.setOption( 'Resources/StorageElements/ProductionSandboxSE/AccessProtocol.1/Port', '9196' )
localCfg.setOption( 'Resources/StorageElements/ProductionSandboxSE/AccessProtocol.1/ProtocolName', 'DIP' )
localCfg.setOption( 'Resources/StorageElements/ProductionSandboxSE/AccessProtocol.1/Path', '%s/sandboxes' % setupName )
localCfg.setOption( 'Resources/StorageElements/ProductionSandboxSE/AccessProtocol.1/Access', 'remote' )



# Setup the DFC
#
# DataManagement
# {
#   Production
#   {
#     Services
#     {
#       FileCatalog
#       {
#         DirectoryManager = DirectoryClosure
#         FileManager = FileManagerPS
#         SecurityManager = FullSecurityManager
#       }
#     }
#     Databases
#       {
#         FileCatalogDB
#         {
#           DBName = FileCatalogDB
#         }
#       }
#   }
# }


for sct in ['Systems/DataManagement',
            'Systems/DataManagement/Production',
            'Systems/DataManagement/Production/URLs',
            'Systems/DataManagement/Production/Services',
            'Systems/DataManagement/Production/Services/FileCatalog',
            'Systems/DataManagement/Production/Databases',
            'Systems/DataManagement/Production/Databases/FileCatalogDB', ]:
  if not localCfg.existsKey( sct ):
    localCfg.createNewSection( sct )

localCfg.setOption( 'Systems/DataManagement/Production/Services/FileCatalog/DirectoryManager', 'DirectoryClosure' )
localCfg.setOption( 'Systems/DataManagement/Production/Services/FileCatalog/FileManager', 'FileManagerPs' )
localCfg.setOption( 'Systems/DataManagement/Production/Services/FileCatalog/SecurityManager', 'FullSecurityManager' )

localCfg.setOption( 'Systems/DataManagement/Production/Databases/FileCatalogDB/DBName', 'FileCatalogDB' )
localCfg.setOption( 'Systems/DataManagement/Production/Databases/FileCatalogDB/Host', 'dbod-dirac-ci.cern.ch' )
localCfg.setOption( 'Systems/DataManagement/Production/Databases/FileCatalogDB/Port', '5501' )

localCfg.writeToFile( localConfigFile )
