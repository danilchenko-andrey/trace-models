#!/bin/bash
rm -rf traces
mkdir traces
for i in {0..50}
do
	echo -n "Doing $i execution..."
	python alarm/train_set_generator.py $1 > alarm-test
	java -cp .:$CLASSPATH daikon.Chicory --daikon alarm.Alarm 2>&1 >/dev/null
	zcat Alarm.dtrace.gz > traces/Alarm.dtrace.$i
	rm Alarm.dtrace.gz
	echo "done"
done
#java daikon.Daikon traces/Alarm.dtrace.*
#java daikon.PrintInvariants Alarm.inv.gz > Alarm.dtrace.invariants
echo -n "Mining 50 executions..."
python /mnt/vbshare/process_dtrace.py 50 traces/Alarm.dtrace > scenarios
cat process-dtrace.log | grep "DECODE" | sed -e 's/.*DECODE. \(.*\) = \(.*\)$/\2 = \1/' | sort | uniq > Alarm.decode
echo "done"
echo -n "Building automaton..."
java -jar /mnt/vbshare/builder.jar scenarios -r Alarm.gv -t Alarm.tree.gv -s 100
echo "done"
echo -n "Decoding..."
cat Alarm.tree.gv | python /mnt/vbshare/decode_gv.py Alarm.decode STATE_ | python /mnt/vbshare/decode_gv.py Alarm.decode var_ > Alarm.tree.decoded.gv
cat Alarm.gv | python /mnt/vbshare/decode_gv.py Alarm.decode STATE_ | python /mnt/vbshare/decode_gv.py Alarm.decode var_ > Alarm.decoded.gv
echo "done"
echo -n "Painting..."
dot -T png Alarm.tree.gv > alarm-tree.png
dot -T png Alarm.gv > alarm.png
dot -T png Alarm.tree.decoded.gv > alarm-tree-decoded.png
dot -T png Alarm.decoded.gv > alarm-decoded.png
echo "done"