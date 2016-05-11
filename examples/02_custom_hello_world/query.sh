#!/usr/bin/env bash -l

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

['../../rules/general_rules'].
[yw_views].
[nw_views].
[yw_nw_views].

set_prolog_flag(unknown, fail).

%-------------------------------------------------------------------------------
banner( 'YW_Q1',
        'What is the name and description of the workflow implemented by the script?',
        'yw_q1(WorkflowName, Description).').
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
        'yw_q2(StepName, Description).').
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
        'Where is the definition of workflow step greet_user?',
        'yw_q3(SourceFile, StartLine, EndLine).').
[user].
:- table yw_q3/3.
yw_q3(SourceFile, StartLine, EndLine) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_workflow_step(_, 'greet_user', WorkflowId, SourceId, StartLine, EndLine),
    yw_source_file(SourceId, SourceFile).
end_of_file.
printall(yw_q3(_,_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q4',
        'What are the names and descriptions of any outputs of the workflow?',
        'yw_q4(OutputName, Description).').
[user].
:- table yw_q4/2.
yw_q4(OutputName, Description) :-
    yw_workflow_script(WorkflowId,_,_,_),
    yw_step_output(WorkflowId, _, _, PortId, _,_, OutputName),
    yw_description(port, PortId, _, Description).
end_of_file.
printall(yw_q4(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q5',
        'What data flows from the accept_greeting workflow step to the greet_user step?',
        'yw_q5(DataName).').
[user].
:- table yw_q5/1.
yw_q5(DataName) :-
    yw_flow(_, 'accept_greeting',_, _, _, DataName, _, _, _, 'greet_user').
end_of_file.
printall(yw_q5(_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'NW_Q1',
        'What functions are called from the top level of the script?',
        'nw_q1(FunctionName).').
[user].
:- table nw_q1/1.
nw_q1(FunctionName) :-
    nw_script_activation(_,_, ScriptActivationId, _),
    nw_function_activation(_, FunctionName, _, ScriptActivationId).
end_of_file.
printall(nw_q1(_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'NW_Q2',
        'What variable values are passed as arguments to the function print_greeting()?',
        'nw_q2(VariableName, Value).').
[user].
:- table nw_q2/2.
nw_q2(VariableName, Value) :-
    nw_function_argument(_, 'print_greeting', _, _, Value, VariableName, VariableId),
    VariableId \== nil.
end_of_file.
printall(nw_q2(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'NW_Q3',
        'What literal values are passed as arguments to the function print_greeting()?',
        'nw_q3(Value).').
[user].
:- table nw_q3/1.
nw_q3(Value) :-
    nw_function_argument(_, 'print_greeting', _, _, Value, _, nil).
end_of_file.
printall(nw_q3(_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_NW_Q1',
        'What Python variables carries what values of custom_greeting into the greet_user workflow step?',
        'yw_nw_q1(VariableId, VariableName, VariableValue).').
[user].
:- table yw_nw_q1/3.
yw_nw_q1(VariableId,VariableName,VariableValue) :-
    yw_step_input(_, _, _, PortId, _, _, 'custom_greeting'),
    nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, _, _, PortId, _, _, _).
end_of_file.
printall(yw_nw_q1(_,_,_)).
%-------------------------------------------------------------------------------

END_XSB_STDIN
