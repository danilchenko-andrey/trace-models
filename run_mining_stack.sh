#!/bin/bash

for i in {0..50}
do
	echo -n "Doing $i execution..."
	python stack/train_set_generator.py $1 > stack-test
	java -cp .:$CLASSPATH daikon.Chicory --daikon stack.StackRunner 2>&1 >/dev/null
	zcat StackRunner.dtrace.gz > traces/StackRunner.dtrace.$i
	echo "done"
done
rm StackRunner.dtrace.gz
#java daikon.Daikon StackRunner.dtrace.[0-9]
#java daikon.PrintInvariants StackRunner.inv.gz > StackRunner.dtrace.invariants
echo -n "Mining executions..."
python /mnt/vbshare/process_dtrace.py 50 traces/StackRunner.dtrace > StackRunner.scenario
cat process-dtrace.log | grep "DECODE" | sed -e 's/.*DECODE. \(.*\) = \(.*\)$/\2 = \1/' | sort | uniq > StackRunner.decode
echo "done"
echo -n "Building automaton..."
java -jar /mnt/vbshare/builder.jar StackRunner.scenario -r StackRunner.gv -t StackRunner.tree.gv -s 2
echo "done"
echo -n "Decoding..."
cat StackRunner.tree.gv | python /mnt/vbshare/decode_gv.py StackRunner.decode > StackRunner.tree.decoded.gv
cat StackRunner.gv | python /mnt/vbshare/decode_gv.py StackRunner.decode > StackRunner.decoded.gv
echo "StackRunner"
echo -n "Painting..."
dot -T png StackRunner.tree.gv > stack-tree.png
dot -T png StackRunner.gv > stack.png
dot -T png StackRunner.tree.decoded.gv > stack-tree-decoded.png
dot -T png StackRunner.decoded.gv > stack-decoded.png
echo "done"