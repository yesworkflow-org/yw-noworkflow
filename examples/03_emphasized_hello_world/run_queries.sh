#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

['../rules/general_rules'].
['../rules/yw_rules'].
['../rules/yw_nw_rules'].
[yw_views].
[nw_facts].


%-------------------------------------------------------------------------------
banner( 'YW_Q1',
        'What is the name and description of the workflow implemented by the script?',
        'yw_q1(WorkflowName, Description)').
[user].
:- table yw_q1/2.
yw_q1(WorkflowName, Description) :-
    yw_workflow_script(WorkflowId, WorkflowName, _,_),
    yw_description(program, WorkflowId, _, Description).
end_of_file.
printall(yw_q1(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q2',
        'What workflow steps comprise the top-level workflow?',
        'yw_q2(StepName, Description)').
[user].
:- table yw_q2/2.
yw_q2(StepName, Description) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_workflow_step(StepId, StepName, WorkflowId, _, _, _),
    yw_description(program, StepId, _, Description).
end_of_file.
printall(yw_q2(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q3',
        'Where is the definition of workflow step emphasize_greeting?',
        'yw_q3(SourceFile, StartLine, EndLine)').
[user].
:- table yw_q3/3.
yw_q3(SourceFile, StartLine, EndLine) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_workflow_step(_, 'emphasize_greeting', WorkflowId, SourceId, StartLine, EndLine),
    yw_source_file(SourceId, SourceFile).
end_of_file.
printall(yw_q3(_,_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q4',
        'What are the names and descriptions of any outputs of the workflow?',
        'yw_q4(OutputName, Description)').
[user].
:- table yw_q4/2.
yw_q4(OutputName, Description) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_out_port(WorkflowId, _, PortId, _,_, OutputName),
    yw_description(port, PortId, _, Description).
end_of_file.
printall(yw_q4(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q5',
        'What data flows from the emphasize_greeting workflow step to the print_greeting step?',
        'yw_q5(DataName)').
[user].
:- table yw_q5/1.
yw_q5(DataName) :-
    yw_flow(_, 'emphasize_greeting', _, DataName, _, 'print_greeting').
end_of_file.
printall(yw_q5(_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'NW_Q1',
        'What functions are called from the top level of the script?',
        'nw_q1(FunctionName)').
[user].
:- table nw_q1/1.
nw_q1(FunctionName) :-
    call_from_top_function(_, FunctionName, _).
end_of_file.
printall(nw_q1(_)).
%-------------------------------------------------------------------------------


END_XSB_STDIN

# %-------------------------------------------------------------------------------
# banner( 'NW_Q2',
#         'What variable values are passed to greet_user() from the top of the script?',
#         'nw_q2(ActivationId, ParameterName, VariableName, Value)').
# [user].
# :- table nw_q2/4.
# nw_q2(ActivationId, ParameterName, VariableName, Value) :-
#     activation_argument_variable(ActivationId, 'greet_user', ParameterName, VariableName, Value).
# end_of_file.
# printall(nw_q2(_,_,_,_)).
# %-------------------------------------------------------------------------------
#
# %-------------------------------------------------------------------------------
# banner( 'NW_Q3',
#         'What literal values are passed to greet_user() from the top of the script?',
#         'nw_q3(ActivationId, Parameter, Value)').
# [user].
# :- table nw_q3/3.
# nw_q3(ActivationId, Parameter, Value) :-
#     activation_argument_literal(ActivationId, 'greet_user', Parameter, Value).
# end_of_file.
# printall(nw_q3(_,_,_)).
# %-------------------------------------------------------------------------------
#
#
# %-------------------------------------------------------------------------------
# banner( 'YW_NW_Q1',
#         'What Python variables carries what values of emphasized_greeting into the print_greeting workflow step?',
#         'yw_nw_q1(VariableId, VariableName, VariableValue)').
# [user].
# :- table yw_nw_q1/3.
# yw_nw_q1(VariableId,VariableName,VariableValue) :-
#     data(DataId,'emphasized_greeting',_),
#     port(PortId, 'in', _, _, _, DataId),
#     nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, PortId).
# end_of_file.
# printall(yw_nw_q1(_,_,_)).
# %-------------------------------------------------------------------------------
