#!/bin/sh 
#-------------------------------------------------------------------------------
# dirac_ci
#
#  Several functions used for Jenkins style jobs
#
#
# fstagni@cern.ch  
# 09/12/2014
#-------------------------------------------------------------------------------

# URLs where to get scripts
DIRAC_INSTALL='https://github.com/DIRACGrid/DIRAC/raw/integration/Core/scripts/dirac-install.py'
DIRAC_PILOT='https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/WorkloadManagementSystem/PilotAgent/dirac-pilot.py'
DIRAC_PILOT_TOOLS='https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/WorkloadManagementSystem/PilotAgent/pilotTools.py'
DIRAC_PILOT_COMMANDS='https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/WorkloadManagementSystem/PilotAgent/pilotCommands.py'


#.............................................................................
#
# function getCertificate:
#  
#   This function just gets a host certificate from a known location 
#
#.............................................................................

function getCertificate(){
	echo '[getCertificate]'

	mkdir -p $WORKSPACE/etc/grid-security/
	cp /root/hostcert.pem $WORKSPACE/etc/grid-security/
	cp /root/hostkey.pem $WORKSPACE/etc/grid-security/ 
	chmod 0600 $WORKSPACE/etc/grid-security/hostkey.pem

} 
	

#...............................................................................
#
# DIRACPilotInstall:
#
#   This function uses the pilot code to make a DIRAC pilot installation
#   The JobAgent is not run here 
#
#...............................................................................

function DIRACPilotInstall(){
	
	#cert first (host certificate)
	getCertificate
	
	#get the necessary scripts
	wget --no-check-certificate -O dirac-install.py $DIRAC_INSTALL
	wget --no-check-certificate -O dirac-pilot.py $DIRAC_PILOT
	wget --no-check-certificate -O pilotTools.py $DIRAC_PILOT_TOOLS
	wget --no-check-certificate -O pilotCommands.py $DIRAC_PILOT_COMMANDS

	#run the dirac-pilot script, only for installing, do not run the JobAgent here
	#FIXME: using LHCb-Certification here, and LHCb CS!
	python dirac-pilot.py -S LHCb-Certification -C dips://lbvobox18.cern.ch:9135/Configuration/Server -N jenkins.cern.ch -Q jenkins-queue_not_important -n DIRAC.Jenkins.ch --cert --certLocation=/home/dirac/certs/ $DEBUG
}
