#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

set_prolog_flag(unknown, fail).

[yw_views].
['../../graphs/graph_rules'].

[user].
graph() :-

    yw_workflow_script(WorkflowId, WorkflowName, _, _),

    graph_begin('YW_DATA', WorkflowName, 'TB'),

    start_visible_cluster_box('workflow'),
    data_node_style(),
    graph_data_nodes(WorkflowId),
    graph_data_to_data_edges(WorkflowId),
    end_cluster_box(),

    start_invisible_cluster_box('inflows'),
    workflow_port_style(),
    graph_inflow_nodes(WorkflowId),
    end_cluster_box(),
    graph_inflow_to_data_edges(WorkflowId),

    start_invisible_cluster_box('outflows'),
    workflow_port_style(),
    graph_outflow_nodes(WorkflowId),
    end_cluster_box(),
    graph_data_to_outflow_edges(WorkflowId),

    graph_end().

end_of_file.

graph().

END_XSB_STDIN
