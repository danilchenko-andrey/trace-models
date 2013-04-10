#!/bin/bash

for i in {0..5}
do
	echo -n "Doing $i execution..."
	python stack/train_set_generator.py $1 > stack-test
	java -cp .:$CLASSPATH daikon.Chicory --daikon stack.StackRunner 2>&1 >/dev/null
	zcat StackRunner.dtrace.gz > StackRunner.dtrace.$i
	echo "done"
done
rm StackRunner.dtrace.gz
java daikon.Daikon StackRunner.dtrace.[0-9]
java daikon.PrintInvariants StackRunner.inv.gz > StackRunner.dtrace.invariants
echo -n "Mining 5 executions..."
python /mnt/vbshare/process_dtrace.py 5 StackRunner.dtrace > StackRunner.scenario
echo "done"
echo -n "Building automaton..."
#java -jar /mnt/vbshare/builder.jar Alarm.scenario -r Alarm.gv -s 4
echo "done"
#rm -rf Alarm.dtrace.*
#dot -T png Alarm.tree.gv > alarm-tree.png
#dot -T png Alarm.gv > alarm.png