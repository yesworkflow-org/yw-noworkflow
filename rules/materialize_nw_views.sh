#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

['facts/nw_facts'].
['../../rules/general_rules'].
['../../rules/nw_views'].

set_prolog_flag(unknown, fail).

rule_banner('nw_script_activation(Script, Command, ScriptActivation, Docstring).').
printall(nw_script_activation(_,_,_,_)).

rule_banner('nw_function_definition(FunctionId, Name, FirstLine, LastLine, Docstring).').
printall(nw_function_definition(_,_,_,_,_)).

rule_banner('nw_function_activation(ActivationId, FunctionId, FunctionName, Line, CallerActivationId).').
printall(nw_function_activation(_,_,_,_,_)).

rule_banner('nw_function_argument(ActivationId, FunctionName, ArgumentId, ArgumentName, Value, VariableName, VariableId)').
printall(nw_function_argument(_,_,_,_,_,_,_)).

rule_banner('nw_variable_assignment(ActivationId, VariableId, VariableName, Line, Value).').
printall(nw_variable_assignment(_,_,_,_,_)).

rule_banner('nw_variable_usage(UsageId, ActivationId, VariableId, VariableName, VariableValue, Line).').
printall(nw_variable_usage(_,_,_,_,_,_)).

rule_banner('nw_variable_dependency(DependencyId, ActivationId, FunctionName, AssignmentLine, DownstreamVarId, DownstreamVarName, UpstreamVarId, UpstreamVarName)').
printall(nw_variable_dependency(_,_,_,_,_,_,_,_)).

END_XSB_STDIN
