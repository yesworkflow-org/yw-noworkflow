#!/usr/bin/env bash

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

[yw_views].
[nw_views].
[yw_nw_views].
['../../rules/general_rules'].
['../../rules/yw_rules'].
['../../rules/nw_rules'].
['../../rules/yw_nw_rules'].

set_prolog_flag(unknown, fail).

%-------------------------------------------------------------------------------banner( 'YW_NW_Q1',
        'What Python variables carries what values of custom_greeting into the greet_user workflow step?',
        'yw_nw_q1(VariableId, VariableName, VariableValue).').
[user].
:- table yw_nw_q1/3.
yw_nw_q1(VariableId,VariableName,VariableValue) :-
    yw_step_input(_, _, _, PortId, _, _, 'provided_greeting'),
    nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, _, _, _, PortId, _, _, _).
end_of_file.
printall(yw_nw_q1(_,_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_NW_Q2',
        'What Python variables are associated with each YW data element in the lineage of displayed_greeting value "Hello World"?',
        'yw_nw_q2(DataId, DataName, VarId, VarName, Value, DownstreamDataId, DownstreamDataName, DownstreamVarId, DownstreamVarName).').
[user].
:- table yw_nw_q2/9.
yw_nw_q2(DataId, DataName, VarId, VarName, Value, DownstreamDataId, DownstreamDataName, DownstreamVarId, DownstreamVarName) :-
    DownstreamDataName = 'displayed_greeting',
    DownstreamVarValue = 'Hello World!',
    yw_workflow_script(WorkflowId, _, _, _),
    yw_data(DownstreamDataId, _, WorkflowId, _),
    nw_variable_for_yw_data(DownstreamVarId, DownstreamVarName, DownstreamVarValue, DownstreamDataId, DownstreamDataName),
    nw_variable_in_yw_lineage_of_nw_variable(_, DataId, DataName, VarId, VarName, Value, DownstreamDataId, DownstreamDataName, DownstreamVarId, DownstreamVarName, DownstreamVarValue).
end_of_file.
printall(yw_nw_q2(_,_,_,_,_,_,_,_,_)).
%-------------------------------------------------------------------------------


END_XSB_STDIN

