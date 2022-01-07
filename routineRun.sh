#!/bin/bash
cd /home/pi/priceTracker
git pull
git checkout routineRun
if python priceTracker.py; then
	git add log.csv
	git commit -m "Price tracker auto update."
	git push origin routineRun
	git checkout master
	git merge --no-edit routineRun
	git push
else
	echo "MyProtein price tracker running on raspberry pi crashed." | mail -s "Price Tracker Bug" yutangutil@gmail.com
fi
git checkout master
