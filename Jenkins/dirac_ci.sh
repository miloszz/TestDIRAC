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

############################################
# List URLs where to get scripts
############################################
DIRAC_INSTALL='https://github.com/DIRACGrid/DIRAC/raw/integration/Core/scripts/dirac-install.py'
DIRAC_PILOT='https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/WorkloadManagementSystem/PilotAgent/dirac-pilot.py'
DIRAC_PILOT_TOOLS='https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/WorkloadManagementSystem/PilotAgent/pilotTools.py'
DIRAC_PILOT_COMMANDS='https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/WorkloadManagementSystem/PilotAgent/pilotCommands.py'

DIRAC_RELEASES='https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/releases.cfg'
############################################


############################################
# General utility functions
############################################

#.............................................................................
#
# findRelease:
#
#   If the environment variable "PRERELEASE" exists, we use a prerelease
#   instead of a regular release ( production-like ).
#   If any parameter is passed, we assume we are on pre-release mode, otherwise, 
#   we assume production. It reads from releases.cfg and picks the latest version
#   which is written to {project,dirac,lhcbdirac}.version
#
#.............................................................................
  
function findRelease(){
	echo '[findRelease]'

	cd $WORKSPACE

    PRE='p[[:digit:]]*'

	if [ ! -z "$DIRACBRANCH" ]
	then
		echo 'Looking for DIRAC branch ' $DIRACBRANCH
	else
		echo 'Running on last one'
	fi

	# Create temporary directory where to store releases.cfg (will be deleted then)
	tmp_dir=`mktemp -d -q`
	cd $tmp_dir
	wget --no-check-certificate -O releases.cfg $DIRAC_RELEASES

	# Match project ( DIRAC ) version from releases.cfg
	# If I don't specify a DIRACBRANCH, it will get the latest "production" release
    
    # First, try to find if we are on a production tag
	if [ ! -z "$DIRACBRANCH" ]
	then
    	projectVersion=`cat releases.cfg | grep [^:]v[[:digit:]]*r[[:digit:]]*p[[:digit:]]* | grep $DIRACBRANCH | head -1 | sed 's/ //g'`
    	
    else
    	projectVersion=`cat releases.cfg | grep [^:]v[[:digit:]]*r[[:digit:]]*p[[:digit:]]* | head -1 | sed 's/ //g'`
    fi
    #    projectVersion=`cat releases.cfg | grep [^:]v[[:digit:]]r[[:digit:]]*$PRE | head -1 | sed 's/ //g'`
	# In case there are no production tags for the branch, look for pre-releases in that branch
	if [ ! "$projectVersion" ]
	then
		if [ ! -z "$DIRACBRANCH" ]
		then
			projectVersion=`cat releases.cfg | grep [^:]v[[:digit:]]*r[[:digit:]]*'-pre' | grep $DIRACBRANCH | head -1 | sed 's/ //g'`
	    else
	    	projectVersion=`cat releases.cfg | grep [^:]v[[:digit:]]*r[[:digit:]]*'-pre' | head -1 | sed 's/ //g'`
	    fi
    fi

	projectVersionLine=`cat releases.cfg | grep -n $projectVersion | cut -d ':' -f 1 | head -1`
	# start := line number after "{"  
	start=$(($projectVersionLine+2))
	# end   := line number after "}"
	end=$(($start+2))
	# versions :=
	versions=`sed -n "$start,$end p" releases.cfg`

	# Extract Externals version
	externalsVersion=`echo $versions | sed s/' = '/'='/g | tr ' ' '\n' | grep Externals | cut -d '=' -f2`

	# Back to $WORKSPACE and clean tmp_dir
	cd $WORKSPACE
	rm -r $tmp_dir

    # PrintOuts
    echo DIRAC:$projectVersion && echo $projectVersion > dirac.version
    echo EXTERNALS:$externalsVersion && echo $externalsVersion > externals.version

}

#.............................................................................
#
# diracInstall:
#
#   This function gets the DIRAC install script defined on $DIRAC_INSTAll and
#   runs it with some hardcoded options. The only option that varies is the 
#   project version, in this case DIRAC version, obtained from the file 'dirac.version' 
#   (which coincides with the project version).
#
#.............................................................................

function diracInstall(){
	echo '[diracInstall]'

	cd $WORKSPACE

	wget --no-check-certificate -O dirac-install $DIRAC_INSTALL
	chmod +x dirac-install
	./dirac-install -r `cat dirac.version` -t server $DEBUG
}



############################################
# Pilot
############################################

#...............................................................................
#
# MAIN function: DIRACPilotInstall:
#
#   This function uses the pilot code to make a DIRAC pilot installation
#   The JobAgent is not run here 
#
#...............................................................................

function DIRACPilotInstall(){
	
	prepareForPilot
	
	#run the dirac-pilot script, the JobAgent won't necessarily match a job
	#FIXME: using LHCb-Certification here, and LHCb CS! Also the version is set, need something smarter 
	python dirac-pilot.py -S LHCb-Certification -r v6r12p7 -C dips://lbvobox18.cern.ch:9135/Configuration/Server -N jenkins.cern.ch -Q jenkins-queue_not_important -n DIRAC.Jenkins.ch --cert --certLocation=/home/dirac/certs/ $DEBUG
}

############################################ 
# Utilities


function getCertificate(){
	echo '[getCertificate]'
	# just gets a host certificate from a known location 
	
	mkdir -p $WORKSPACE/etc/grid-security/
	cp /root/hostcert.pem $WORKSPACE/etc/grid-security/
	cp /root/hostkey.pem $WORKSPACE/etc/grid-security/ 
	chmod 0600 $WORKSPACE/etc/grid-security/hostkey.pem

} 

function prepareForPilot(){
	
	#cert first (host certificate)
	getCertificate
	
	#get the necessary scripts
	wget --no-check-certificate -O dirac-install.py $DIRAC_INSTALL
	wget --no-check-certificate -O dirac-pilot.py $DIRAC_PILOT
	wget --no-check-certificate -O pilotTools.py $DIRAC_PILOT_TOOLS
	wget --no-check-certificate -O pilotCommands.py $DIRAC_PILOT_COMMANDS

}
