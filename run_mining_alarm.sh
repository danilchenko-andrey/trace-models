#!/bin/bash

for i in {0..5}
do
	echo -n "Doing $i execution..."
	python alarm/train_set_generator.py $1 > alarm-test
	java -cp .:$CLASSPATH daikon.Chicory --daikon alarm.Alarm 2>&1 >/dev/null
	zcat Alarm.dtrace.gz > Alarm.dtrace.$i
	echo "done"
done
rm Alarm.dtrace.gz
java daikon.Daikon Alarm.dtrace.*
java daikon.PrintInvariants Alarm.inv.gz > Alarm.dtrace.invariants
echo -n "Mining 5 executions..."
python /mnt/vbshare/process_dtrace.py 5 Alarm.dtrace > Alarm.scenario
echo "done"
echo -n "Building automaton..."
#java -jar /mnt/vbshare/builder.jar Alarm.scenario -r Alarm.gv -s 4
echo "done"
#rm -rf Alarm.dtrace.*
#dot -T png Alarm.tree.gv > alarm-tree.png
#dot -T png Alarm.gv > alarm.png