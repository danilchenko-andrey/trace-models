#!/bin/bash

SHARE="/mnt/vbshare"
python $SHARE/process_dtrace.py ru.ezhiki.srez.telephone.Automat Telephone.dtrace > scenarios$1
java -jar $SHARE/builder.jar scenarios$1 -r tmp-scenario.gv -s $2
cat tmp-scenario.gv | sed -e 's/_eq_/=/g' > scenario$1.gv
rm tmp-scenario.gv
dot -Tpng scenario$1.gv > scenario$1.png

mkdir -p $SHARE/results
cp scenario$1.png $SHARE/results/scenario$1.png
