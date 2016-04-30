#!/usr/bin/env bash -l

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

['../rules/general_rules'].
['../rules/yw_rules'].
['../rules/yw_nw_rules'].
[yw_extract_facts].
[yw_model_facts].
[nw_facts].

%-------------------------------------------------------------------------------
banner( 'YW_Q1',
        'What is the name and description of the workflow implemented by the script?',
        'yw_q1(WorkflowName, Description)').
[user].
:- table yw_q1/2.
yw_q1(WorkflowName,Description) :-
    top_workflow(W, WorkflowName),
    program_description(W, Description).
end_of_file.
printall(yw_q1(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q2',
        'What workflow steps comprise the top-level workflow?',
        'yw_q2(StepName, Description)').
[user].
:- table yw_q2/2.
yw_q2(StepName,Description) :-
    top_workflow(W, _),
    has_subprogram(W, P),
    program(P, _, StepName, _, _),
    program_description(P, Description).
end_of_file.
printall(yw_q2(_,_)).
%-------------------------------------------------------------------------------


%-------------------------------------------------------------------------------
banner( 'YW_Q3',
        'Where is the definition of workflow step HelloWorld.print_greeting?',
        'yw_q3(SourceFile, StartLine, EndLine)').
[user].
:- table yw_q3/3.
yw_q3(SourceFile, StartLine, EndLine) :-
    program_source('HelloWorld.print_greeting', SourceFile, StartLine, EndLine).
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
    top_workflow(W,_),
    has_out_port(W, P),
    port(P, _, OutputName, _, _, _),
    port_description(P, Description).
end_of_file.
printall(yw_q4(_,_)).
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


%-------------------------------------------------------------------------------
banner( 'YW_NW_Q1',
        'What functions are called from within the workflow step HelloWorld.print_greeting?',
        'yw_nw_q1(FunctionName)').
[user].
:- table yw_nw_q1/1.
yw_nw_q1(FunctionName) :-
    call_from_workflow_step('HelloWorld.print_greeting', FunctionName, _, _).
end_of_file.
printall(yw_nw_q1(_)).
%-------------------------------------------------------------------------------

END_XSB_STDIN
