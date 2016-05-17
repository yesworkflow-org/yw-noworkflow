#!/usr/bin/env bash -l

ProvidedDataName=$1

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

set_prolog_flag(unknown, fail).

[yw_views].
['../../graphs/graph_rules'].

[user].
graph() :-

    yw_workflow_script(W, WorkflowName, _, _),
    yw_data(D, $ProvidedDataName, W, _),

    gv_graph('yw_data_view', WorkflowName, 'TB'),

        gv_cluster('workflow', 'black'),
            gv_node_style_atomic_steps(),
            gv_atomic_step_nodes_upstream_of_data(W,D),
            gv_node_style_composite_steps(),
            gv_composite_step_nodes_upstream_of_data(W,D),
            gv_node_style_data(),
            gv_data_nodes_upstream_of_data(W,D),
            gv_node_style_param(),
            gv_param_nodes_upstream_of_data(W,D),
        gv_cluster_end(),

        gv_cluster('inflows', 'white'),
            gv_node_style_workflow_port(),
            gv_inflow_nodes_upstream_of_data(W,D),
        gv_cluster_end(),

        gv_cluster('outflows', 'white'),
            gv_node_style_workflow_port(),
            gv_outflow_node_for_data(W,D),
        gv_cluster_end(),

        gv_data_to_step_edges_upstream_of_data(W,D),
        gv_step_to_data_edges_upstream_of_data(W,D),
        gv_inflow_to_data_edges_upstream_of_data(W,D),
        gv_data_to_outflow_edges_upstream_of_data(W,D),

    gv_graph_end().

end_of_file.

graph().

END_XSB_STDIN
