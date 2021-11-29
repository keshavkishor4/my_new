#!/bin/bash
#Author - Daniel Dhanaraj - daniel_dhanaraj@optum.com
#Purpose - The script will monitor the status of each EAR deployed to each JVM and restart the JVM if an application is unre#sponsive.  The script uses wget to monitor the status of the URL
shopt -s expand_aliases
source /etc/profile.d/aemprofile.sh

inputFile="/home/wsuser/webapp/scripts/eiMonInput.txt"
scriptLog="/home/wsuser/webapp/log/eiUrlMonitor.log"
statusCode="200|401|403"
sender="EAIMonitoringSystem@EIJumpServer.com"
hName=`hostname`
profileName=""
jvmRStatus="no"
noMonLen="0"
lckPresent="no"
noCert="--no-check-certificate"

chkLock()
{
if [  -f $lckfile ]; then
        echo "Environment is locked by another process so cant proceed with restart"
        lckPresent="yes"
else
        lckPresent="no"
fi
}


aemJvmRestart()
{
        stopaem
        jvmPID=`ps -eaf|grep java|grep aem|grep -v "grep" |awk '{print $ 2}'`
        if [[ "" != $jvmCheck ]];then
                kill -9 $jvmPID
        fi
        sleep 150
        startaem
        if [ $? -eq 0 ];then
                echo -e "The JVM - $1  started succesfully\n" >>  ${wgetOut}/mailout.txt
                jvmRStatus="yes"
        else
                echo -e "Problem starting the JVM - $1, please check\n" >>  ${wgetOut}/mailout.txt
        fi
}

monitorURL()
{
	wget -nc --delete-after -T 30 -w 10 -t 1 $noCert $url 2> $wgetOut/${hName}_out.txt
        egrep "200|401|403|404|302" $wgetOut/${hName}_out.txt
        if [ $? -ne 0 ]; then
        	echo -e "`date` ---- There is problem in the URL monitoring ----> $hName - $url \n" >> ${wgetOut}/mailout.txt
                jvmRStatus="no"
                echo -e "Starting the AEM process \n" >> ${wgetOut}/mailout.txt
                if [ $jvmRStatus == "no" ];then
                	#chkLock
                        if [ $lckPresent == "no" ];then
				aemJvmRestart									
                        else
                                echo -e "The JVM is being restarted as part of the earlier URL failure" >> ${wgetOut}/mailout.txt
                        fi
                        jvmRStatus="yes"
                        echo "" >> ${wgetOut}/mailout.txt
                fi
                rm -rf $cxtRoot
	fi
}


sendAlert()
{
if [ -f ${wgetOut}/mailout.txt ]; then
        cat ${wgetOut}/mailout.txt | mail -r $sender -s "URL probe failure on $hName" -c "${cdL}" $tdL
        rm -rf ${wgetOut}/mailout.txt
fi
}


readInput(){
        . $inputFile
        hostOS=`uname`
        if [ ${hostOS} = "Linux" ] ; then
                monitorURL
                sendAlert
        fi
}


echo "The script start time is " `date` > $scriptLog
readInput
echo "The script end time is " `date` >> $scriptLog
