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
            'Systems/DataManagement/Production/Databases',
            'Systems/DataManagement/Production/Databases/FileCatalogDB' ]:
  if not localCfg.existsKey( sct ):
    try:
      res = localCfg.createNewSection( sct )
      print res
    except KeyError, ke:
      print ke

res = localCfg.setOption( 'Systems/DataManagement/Production/Databases/FileCatalogDB/DBName', 'FileCatalogDB' )
print res
res = localCfg.setOption( 'Systems/DataManagement/Production/Databases/FileCatalogDB/Host', 'db-50098.cern.ch' )
print res
res = localCfg.setOption( 'Systems/DataManagement/Production/Databases/FileCatalogDB/Port', '5501' )
print res

res = localCfg.writeToFile( localConfigFile )
print res
