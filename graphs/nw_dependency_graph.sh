#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

set_prolog_flag(unknown, fail).

['facts/nw_facts'].
['../../graphs/graph_rules'].
['../../graphs/yw_graph_rules'].

[user].
graph :-

    gv_graph('nw_dependencies', 'Dependencies', 'TB'),
        gv_edges__nw_dependencies,
    gv_graph_end.

end_of_file.

graph.

END_XSB_STDIN
