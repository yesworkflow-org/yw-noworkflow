rm -rf facts.db

FILE=*.csv

for f in $FILE
do
 NAME=`echo "$f" | cut -d'.' -f1`
 MESSAGE=".mode csv\n.import $f $NAME"
 echo -e $MESSAGE | sqlite3 facts.db
 # do something on $f
done

python extract_query.py > extract_query_output.txt
python model_query.py > model_query_output.txt
