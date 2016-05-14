#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

set_prolog_flag(unknown, fail).

[yw_views].
['../../graphs/graph_rules'].

[user].
graph() :-

    yw_workflow_script(W, WorkflowName, _, _),

    gv_graph('yw_data_view', WorkflowName, 'TB'),

        gv_cluster('workflow', 'black'),
            gv_node_style_atomic_steps(),
            gv_atomic_step_nodes(W),
            gv_node_style_composite_steps(),
            gv_composite_step_nodes(W),
        gv_cluster_end(),

        gv_cluster('inflows', 'white'),
            gv_node_style_workflow_port(),
            gv_inflow_nodes(W),
        gv_cluster_end(),

        gv_cluster('outflows', 'white'),
            gv_node_style_workflow_port(),
            gv_outflow_nodes(W),
        gv_cluster_end(),

        gv_step_to_step_edges(W),
        gv_inflow_to_program_edges(W),
        gv_program_to_outflow_edges(W),

    gv_graph_end().

end_of_file.

graph().

END_XSB_STDIN
