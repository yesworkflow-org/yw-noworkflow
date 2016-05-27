#!/usr/bin/env bash -l
#
# ./run_queries.sh &> run_queries.txt

xsb --quietload --noprompt --nofeedback --nobanner << END_XSB_STDIN

['facts/nw_facts'].
['../../rules/general_rules'].
['../../rules/nw_views'].

set_prolog_flag(unknown, fail).

rule_banner('nw_script_activation(Script, Command, ScriptAct, Docstring).').
printall(nw_script_activation(_,_,_,_)).

rule_banner('nw_function_definition(FuncId, Name, FirstLine, LastLine, Docstring).').
printall(nw_function_definition(_,_,_,_,_)).

rule_banner('nw_function_activation(ActId, FuncId, FuncName, Line, CallerActId).').
printall(nw_function_activation(_,_,_,_,_)).

rule_banner('nw_function_argument(ActId, FuncName, LocalVarId, LocalVarName, Value, Type, CallerVarName, CallerVarId)').
printall(nw_function_argument(_,_,_,_,_,_,_,_)).

rule_banner('nw_variable_assignment(ActId, VarId, VarName, Line, Value).').
printall(nw_variable_assignment(_,_,_,_,_)).

rule_banner('nw_variable_usage(UsageId, ActId, VariableId, VarName, VarValue, Line).').
printall(nw_variable_usage(_,_,_,_,_,_)).

rule_banner('nw_variable_dependency(Why, ActId, FuncName, AssignmentLine, DownstreamVarId, DownstreamVarName, UpstreamVarId, UpstreamVarName)').
printall(nw_variable_dependency(_,_,_,_,_,_,_,_)).

END_XSB_STDIN
