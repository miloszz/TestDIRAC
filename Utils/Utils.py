import os, shutil

def cleanTestDir():
  for fileIn in os.listdir( '.' ):
    if 'Local' in fileIn:
      shutil.rmtree( fileIn )
    for fileToRemove in ['std.out', 'std.err']:
      try:
        os.remove( fileToRemove )
      except OSError:
        continue
