#!/bin/bash
# Crontab use eg.:
#	0 */2 * * * /home/me/ts3sniff/generate.sh /home/me/teamspeak/logs
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $1
latestlogfile=$(pwd)/$(ls -t *.log | head -1)

cd $DIR
python sniff.py $latestlogfile --weeks 4
python analysis.py