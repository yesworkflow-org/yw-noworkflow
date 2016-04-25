#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb << END_XSB_STDIN

[yw_extract].
[yw_model].
[nw].
[yw_rules].
[yw_nw_rules].
[queries].

printall(yw_q1_desc(_), yw_q1(_,_)).
printall(yw_q2_desc(_), yw_q2(_,_)).
printall(yw_q3_desc(_), yw_q3(_,_,_)).

printall(nw_q1_desc(_), nw_q1(_,_)).


END_XSB_STDIN
