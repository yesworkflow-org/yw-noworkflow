#!/usr/bin/env bash -l

# This script is NOT meant to be executed "as is".
# Rather this is for copy-pasting, one command at a time,
# while explaining what's going on. 

# Get the docker image (note: use "sudo" on Linux), using an explicit version id: 
docker run -it -v $HOME:$HOME yesworkflow/yw-noworkflow:0.2.0.6

# change into demo directory 
cd simulate_data_collection

# shorten prompt 
export PS1='$ '

# remove all derived products
rm -rf facts .noworkflow *.xwam *.gv *.png *.pdf *.P *.txt ../../rules/*.xwam

# for database facts
mkdir -p facts

# run YesWorkflow on the script to extract YW facts and model
java -jar /home/yw/bin/yesworkflow-0.2.0.jar model simulate_data_collection.py -c extract.language=python -c extract.factsfile=facts/yw_extract_facts.P -c model.factsfile=facts/yw_model_facts.P -c query.engine=xsb

# create some high-level YW views
bash ../../scripts/materialize_yw_views.sh > yw_views.P

# Now run the actual script using noWorkflow as the provenance recorder
now run -e Tracer -d 3 simulate_data_collection.py q55 --cutoff 12 --redundancy 0 | cut -c 21- > run_outputs.txt

# Generate the complete big "monster" runtime provenance graph
now dataflow -d 2 -m simulation > nw_monster.gv

# ... and render with Graphviz
dot -Tpdf nw_monster.gv -o nw_monster.pdf 

# remove an output file (for testing, debugging purposes!?)
rm -f run/data/DRT240/DRT240_12000eV_002.img

# Doesn't this exist already? 
mkdir -p facts

# output the noWorkflow SQL schema
now schema -d sql > nw_schema.gv
dot -Tpdf nw_schema.gv -o nw_schema.pdf

# output the noWorkflow Prolog schema
now schema -d prolog > nw_schema.gv
dot -Tpdf nw_schema.gv -o nw_schema.pdf

# export noWorkflow facts from the last trial  
now export -t -m dependency | grep -v 'environment(' > facts/nw_facts.P

# generate derived facts
bash ../../scripts/materialize_nw_views.sh > nw_views.P
bash ../../scripts/materialize_yw_nw_views.sh > yw_nw_views.P

# run queries
bash query.sh > query_outputs.txt

# generate graphs as gv/dot files (Graphviz) 
bash ../../scripts/yw_data_graph.sh > yw_data_graph.gv
bash ../../scripts/yw_process_graph.sh > yw_process_graph.gv
bash ../../scripts/yw_combined_graph.sh > yw_combined_graph.gv
bash ../../scripts/yw_prospective_lineage.sh \
	corrected_image \
	> yw_prospective_lineage.gv
bash ../../scripts/yw_nw_retrospective_lineage.sh \
	corrected_image 'run/data/DRT240/DRT240_11000eV_002.img' \
	> yw_nw_retrospective_lineage.gv

# create df_style helper that can be used to change noWorkflow graph style
now helper df_style.py

# export filtered noWorkflow simulation graph with depth 2
now dataflow -d 2 -v 55 -f 'run/data/DRT240/DRT240_11000eV_002.img' -m simulation | python df_style.py -d BT -e > nw_filtered_lineage_graph.gv
dot -Tpdf nw_filtered_lineage_graph.gv -o nw_filtered_lineage_graph.pdf


# render graphs using dot (Graphviz)
dot -Tpdf yw_data_graph.gv -o yw_data_graph.pdf
dot -Tpdf yw_process_graph.gv -o yw_process_graph.pdf
dot -Tpdf yw_combined_graph.gv -o yw_combined_graph.pdf
dot -Tpdf yw_prospective_lineage.gv -o yw_prospective_lineage.pdf
dot -Tpdf yw_nw_retrospective_lineage.gv -o yw_nw_retrospective_lineage.pdf
