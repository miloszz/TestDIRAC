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
