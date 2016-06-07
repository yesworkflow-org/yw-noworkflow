#!/usr/bin/env bash

DataName=$1
DataValue=$2

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

set_prolog_flag(unknown, fail).

['./facts/nw_facts'].
[yw_views].
[nw_views].
[yw_nw_views].
['../../rules/yw_rules'].
['../../rules/nw_rules'].
['../../rules/yw_nw_rules'].
['../../rules/gv_rules'].
['../../rules/yw_graph_rules'].

[user].

graph :-

    V = '$DataValue',
    yw_workflow_script(W, WorkflowName, _, _),
    yw_data(D, '$DataName', W, _),

    gv_graph('yw_data_view', WorkflowName, 'TB'),
        gv_cluster('workflow', 'black'),
            gv_nodestyle__atomic_step_invocation,
            gv_nodes__atomic_steps__upstream_of_data(W,D),
            gv_nodestyle__subworkflow,
            gv_nodes__subworkflows__upstream_of_data(W,D),
            gv_nodestyle__data_value,
            gv_nodes__data_values__upstream_of_data_product(D,V),
            gv_nodestyle__param_value,
            gv_nodes__param_values__upstream_of_data_product(D,V),
        gv_cluster_end,

        gv_cluster('inflows', 'white'),
            gv_node_style__workflow_port,
            gv_nodes__inflows__upstream_of_data(W,D),
        gv_cluster_end,

        gv_cluster('outflows', 'white'),
            gv_node_style__workflow_port,
            gv_node__outflow_for_data(W,D),
        gv_cluster_end,

        gv_edges__data_to_step__upstream_of_data(W, D),
        gv_edges__step_to_data__upstream_of_data(W, D),
        gv_edges__inflow_to_data__upstream_of_data(W, D),
        gv_edges__data_to_outflow__upstream_of_data(W, D),

    gv_graph_end.

end_of_file.

graph.

END_XSB_STDIN
