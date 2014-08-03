#!/bin/sh

# Exemple :
# ./run.sh DATA/export_csa/

if [ "$1" != "" ]
then
  data="$1"
else
  data=.
fi

# Attention, ces paramètres sont codés en dur dans indicators.py
resdir=Resultats
csv=$resdir/indicators.csv

test -d $resdir || mkdir $resdir
test -f $csv && mv -i $csv $resdir/backup.csv
echo 'identifiant ego;;id csa;nb amis;nb liens;nb com Louvain;nb amis max CC;nb com Louvain max CC;diametre;nb amis isoles;modularite;coeff clustering;densite' > $csv

for ego in $data/????????????????????????????*
do
    echo $ego
    python indicators.py $ego
done

