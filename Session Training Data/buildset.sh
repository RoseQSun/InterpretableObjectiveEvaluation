#!/bin/bash

cp $1 temp.txt

lines=(`cat temp.txt | grep -n "X:" | awk '{split($0,c,":"); print c[1]}'`)
for ii in `seq 0 $((${#lines[@]}-2))`; do
  echo $(($ii+1)) "of" $((${#lines[@]}-1))
  echo "X:"$ii > sessiontune
  commd=`echo ${lines[$ii]},$((lines[$((ii+1))]-1))p";"$((lines[$((ii+1))]-1))q`
  sed -n $commd temp.txt | sed '/^$/d' | sed 's/ //g' | tail -n3 >> sessiontune
  abc2midi sessiontune
done
