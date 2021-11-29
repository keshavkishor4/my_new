#!/bin/bash
set -x

scriptHome="/home/wsuser/webapp/work/"
inputFile="/home/wsuser/webapp/scripts/eiMonInput.txt"
scriptLog="/home/wsuser/webapp/log/eiMonitor.log"
host=`hostname`
tPeriod=`date`

function diskUsageMon(){
        dFile=${workDir}/diskUsage.txt
        if [ ${#omitList} -gt 0 ]; then
                dskParUsage=`df -P  |grep -vE "^[^/]|${omitList}" |awk '{print $5, $6}' | sed "s/%//"`
        else
                dskParUsage=`df -P |grep -E "/ebiz|/wastmp|/ebiz/app_logs"|grep -v "nas"| awk '{print $5, $6}' | sed "s/%//"`
        fi
        echo "$dskParUsage" | while read percent fs
        do
        if [ $percent -ge $diskThresh ];then
                echo "The configured threshold for this monitor is $diskThresh " >> $dFile
                echo "Currernt disk space usage for $fs is $percent%" >> $dFile
                echo "" >> $dFile
        fi
        done
        if [ -f ${dFile} ];then
                cat $dFile |mail -r $sender -s "Disk Space Threshold reached on server $host - $tPeriod" -c "${cdL}" $tdL
                cat $dFile  > $scriptLog
                rm -f $dFile
        fi
}



function memUsageMon(){
        mFile=${workDir}/memUsage.txt
        totalMem=`free -mt | grep Mem | awk '{print $2}'`
        usedMem=`free -mt | grep Mem | awk '{print $4}'`
        totFreeMem=$(($totalMem-$usedMem))
        freePercent=$((100*$totFreeMem/$totalMem))
        echo "THE FREE PERCENT IS " $freePercent
        if [[ "$freePercent" -le $memThresh  ]]; then
                echo "The configured threshold for this monitor is free memory is less than $memThresh " >> $mFile
                echo "The current free memory is $totFreeMem MB ($freePercent % of $totalMem MB memory)" >> $mFile
                echo "" >> $mFile
                echo "Top 10 processes using memory:" >> $mFile
                echo "===============================" >> $mFile
                ps -eo pid,ppid,cmd,%mem,rss,%cpu --sort -rss |head >> $mFile
                cat $mFile |mail -r $sender -s "Memory Threshold alert on server $host - $tPeriod" -c "${cdL}" $tdL
                cat $mFile  > $scriptLog
        fi
        rm -rf $mFile
}



function loadAvgMon(){
        cores=`cat /proc/cpuinfo | grep 'processor' | wc -l`
        cores=`echo $cores|xargs`
        fiveMinLoad=`cat /proc/loadavg |awk '{print $2}'`
        fiveMinLoadWhole=`echo $fiveMinLoad | awk '{print int($1+0.5)}'`
        lFile=${workDir}/loadAvg.txt
        load=`cat /proc/loadavg | awk '{print $1}'`
        if [[ $fiveMinLoadWhole > $cores ]]; then
                echo "The last 5 min load average on the system is $fiveMinLoad  on a $cores core system - Please check"  >> $lFile
                echo " " >> $lFile
                echo "System load for this entire day:" >> $lFile
                echo "================================" >> $lFile
                sar -q >> $lFile
                cat $lFile | mail -r $sender -s"Load Average high on server - $host" -c "${cdL}" $tdL
                cat $lFile  > $scriptLog
        fi
        rm -rf $lFile

}


readInput(){
. $inputFile

hostOS=`uname`
if [ ${hostOS} = "Linux" ] ; then
diskUsageMon
memUsageMon
loadAvgMon
fi

}
echo "The script start time is " `date` > $scriptLog
readInput
echo "The script end time is " `date` >> $scriptLog
