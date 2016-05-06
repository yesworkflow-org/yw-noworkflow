#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

[nw_facts].
['../rules/general_rules'].
['../rules/nw_view_rules'].

writeln(''),
writeln(''),
writeln('%---------------------------------------------------------------------------------------------------'),
writeln('% FACT: nw_script_activation(Script, Command, ScriptActivation, Docstring).').
writeln('%...................................................................................................').
printall(nw_script_activation(_,_,_,_)).

writeln(''),
writeln(''),
writeln('%---------------------------------------------------------------------------------------------------'),
writeln('% FACT: nw_function_definition(FunctionId, Name, FirstLine, LastLine, Docstring).').
writeln('%...................................................................................................').
printall(nw_function_definition(_,_,_,_,_)).

writeln(''),
writeln(''),
writeln('%---------------------------------------------------------------------------------------------------'),
writeln('% FACT: nw_function_activation(ActivationId, Name, Line, CallerActivationId).').
writeln('%...................................................................................................').
printall(nw_function_activation(_,_,_,_)).

writeln(''),
writeln(''),
writeln('%---------------------------------------------------------------------------------------------------'),
writeln('% FACT: nw_function_argument(ActivationId, FunctionName, ArgumentName, ArgumentId, Value, VariableName, VariableId)').
writeln('%...................................................................................................').
printall(nw_function_argument(_,_,_,_,_,_,_)).

writeln(''),
writeln(''),
writeln('%---------------------------------------------------------------------------------------------------'),
writeln('% FACT: nw_variable_assignment(ActivationId, VariableId, Name, Line, Value).').
writeln('%...................................................................................................').
printall(nw_variable_assignment(_,_,_,_,_)).

writeln(''),
writeln(''),
writeln('%---------------------------------------------------------------------------------------------------'),
writeln('% FACT: nw_variable_usage(UsageId, ActivationId, VariableId, Name, Line).').
writeln('%...................................................................................................').
printall(nw_variable_usage(_,_,_,_,_,_)).

writeln(''),
writeln(''),
writeln('%---------------------------------------------------------------------------------------------------'),
writeln('% FACT: nw_variable_dependency(DependencyId, DownstreamActId, DownstreamActName,').
writeln('%                              DownstreamVarId, DownstreamVarName,UpstreamActId,').
writeln('%                              UpstreamActName, UpstreamVarId, UpstreamVarName).').
writeln('%...................................................................................................').
printall(nw_variable_dependency(_,_,_,_,_,_,_,_,_)).

END_XSB_STDIN

# writeln('% FACT: nw_function_call(FunctionId, FunctionCallId, Name).').
# printall(nw_function_call(_,_,_)).
# writeln('').
