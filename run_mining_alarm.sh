#!/bin/bash
rm -rf traces
mkdir traces
for i in {0..10}
do
	echo -n "Doing $i execution..."
	python alarm/train_set_generator.py $1 > alarm-test
	java -cp .:$CLASSPATH daikon.Chicory --daikon alarm.Alarm 2>&1 >/dev/null
	zcat Alarm.dtrace.gz > traces/Alarm.dtrace.$i
	rm Alarm.dtrace.gz
	echo "done"
done
java daikon.Daikon traces/Alarm.dtrace.*
#java daikon.PrintInvariants Alarm.inv.gz > Alarm.dtrace.invariants
echo -n "Mining 10 executions..."
python /mnt/vbshare/process_dtrace.py 10 traces/Alarm.dtrace > scenarios
echo "done"
echo -n "Building automaton..."
java -jar /mnt/vbshare/builder.jar scenarios -r Alarm.gv -s 100
echo "done"
dot -T png Alarm.tree.gv > alarm-tree.png
dot -T png Alarm.gv > alarm.png