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


for sct in ['Systems/DataManagement/Production/Services',
            'Systems/DataManagement/Production/Services/FileCatalog' ]:
  if not localCfg.existsKey( sct ):
    try:
      localCfg.createNewSection( sct )
    except KeyError:
      continue

localCfg.setOption( 'Systems/DataManagement/Production/Services/FileCatalog/DirectoryManager', 'DirectoryClosure' )
localCfg.setOption( 'Systems/DataManagement/Production/Services/FileCatalog/FileManager', 'FileManagerPs' )
localCfg.setOption( 'Systems/DataManagement/Production/Services/FileCatalog/SecurityManager', 'DirectorySecurityManagerWithDelete' )
localCfg.setOption( 'Systems/DataManagement/Production/Services/FileCatalog/UniqueGUID', True )


localCfg.writeToFile( localConfigFile )
