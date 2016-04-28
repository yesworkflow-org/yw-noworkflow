#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

[yw_extract_facts].
[yw_model_facts].
[nw_facts].
['../rules/yw_rules'].
['../rules/yw_nw_rules'].

banner('yw_q1(WorkflowName,Description) % What is the name and description of the workflow implemented by the script?').
[user].
:- table yw_q1/2.
yw_q1(WorkflowName,Description) :-
    top_workflow(W, WorkflowName),
    program_description(W, Description).
end_of_file.
printall(yw_q1(_,_)).

banner('yw_q2(StepName,Description) % What workflow steps comprise the top-level workflow?').
[user].
:- table yw_q2/2.
yw_q2(StepName,Description) :-
    top_workflow(W, _),
    has_subprogram(W, P),
    program(P, StepName, _, _, _),
    program_description(P, Description).
end_of_file.
printall(yw_q2(_,_)).

banner('yw_q3(SourceFile,StartLine,EndLine) % Where is the definition of workflow step CustomHelloWorld.greet_user?').
[user].
:- table yw_q3/3.
yw_q3(SourceFile, StartLine, EndLine) :-
    program_source('CustomHelloWorld.greet_user', SourceFile, StartLine, EndLine).
end_of_file.
printall(yw_q3(_,_,_)).

banner('yw_q4(OutputName,Description) % What are the names and descriptions of any outputs of the script?').
[user].
:- table yw_q4/2.
yw_q4(OutputName, Description) :-
    top_workflow(W,_),
    has_out_port(W, P),
    port(P, _, OutputName, _, _, _),
    port_description(P, Description).
end_of_file.
printall(yw_q4(_,_)).

banner('yw_q5(ChannelName) % What data flows from the accept_greeting workflow step to the greet_user step?').
[user].
:- table yw_q5/1.
yw_q5(DataName) :-
    program(AcceptGreetingStep,'accept_greeting',_,_,_),
    has_out_port(AcceptGreetingStep,OutPort),
    port_connects_to_channel(OutPort,Channel),
    channel(Channel,Data),
    data(Data,DataName,_),
    port_connects_to_channel(InPort,Channel),
    has_in_port(GreetUserStep,InPort),
    program(GreetUserStep,'greet_user',_,_,_).
end_of_file.
printall(yw_q5(_)).

banner('nw_q1(FunctionName,CallLine) % What functions are called from the top level of the script?').
[user].
:- table nw_q1/1.
nw_q1(FunctionName) :-
    call_from_top_function(_, FunctionName, _).
end_of_file.
printall(nw_q1(_)).

banner('nw_q2(ActivationId,ParameterName,VariableName,Value) % What variable values are passed to print_greeting() from the top of the script?').
[user].
:- table nw_q2/4.
nw_q2(ActivationId, ParameterName, VariableName, Value) :-
    activation_argument_variable(ActivationId, 'print_greeting', ParameterName, VariableName, Value).
end_of_file.
printall(nw_q2(_,_,_,_)).

banner('nw_q3(ActivationId,Parameter,Value) % What literal values are passed to print_greeting() from the top of the script?').
[user].
:- table nw_q3/3.
nw_q3(ActivationId, Parameter, Value) :-
    activation_argument_literal(ActivationId, 'print_greeting', Parameter, Value).
end_of_file.
printall(nw_q3(_,_,_)).

banner('yw_nw_q1(VariableName,VariableId,VariableValue)) % What Python variables carries what values of custom_greeting into the greet_user workflow step?').
[user].
:- table yw_nw_q1/3.
yw_nw_q1(VariableName,VariableId,VariableValue) :-
    data(DataId,'custom_greeting',_),
    port(PortId, 'in', _, _, _, DataId),
    nw_variable_for_yw_in_port(VariableName, VariableId, VariableValue, PortId).
end_of_file.
printall(yw_nw_q1(_,_,_)).

END_XSB_STDIN
