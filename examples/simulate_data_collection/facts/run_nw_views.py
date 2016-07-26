import sqlite3

def nw_script_activation():
    """
        nw_script_activation(Script, Command, ScriptActId, Docstring) :-
        trial(_,_,_, Script, _, Command, _,_,_, Docstring),
        activation(_, ScriptActId, _,_,_,_, nil).
        
        """
    view = """DROP TABLE IF EXISTS nw_script_activation;
        CREATE TABLE nw_script_activation AS
        SELECT t.script, t.command, a.id act_id, t.docstring
        FROM nw.trial t, nw.function_activation a
        WHERE a.caller_id IS NULL;
        """
    cursor.executescript(view)

def nw_function_definition():
    """
        nw_function_definition(FuncId, FuncName, FirstLine, LastLine, Docstring) :-
        function_def(_, FuncId, FuncName, _, FirstLine, LastLine, Docstring).
        """
    view = """DROP TABLE IF EXISTS nw_function_definition;
        CREATE TABLE nw_function_definition AS
        SELECT def.id func_id, def.name func_name, def.first_line, def.last_line, def.docstring FROM nw.function_def def;
        """
    cursor.executescript(view)

def nw_function_activation():
    """
        nw_function_activation(ActId, FuncId, FuncName, CallerLine, CallerActivationId) :-
            activation(_, ActId, FuncName, CallerLine, _, _, CallerActivationId),
            nw_function_definition(FuncId, FuncName, _, _, _).
        nw_function_activation(ActId, nil, FuncName, CallerLine, CallerActivationId) :-
            activation(_, ActId, FuncName, CallerLine, _, _, CallerActivationId),
            not nw_function_definition(_, FuncName, _, _, _).
        """
    view = """DROP TABLE IF EXISTS nw_function_activation;
        CREATE TABLE nw_function_activation AS
        SELECT DISTINCT a.id act_id, def.func_id func_id, def.func_name func_name, a.line caller_line, a.caller_id
        FROM nw.function_activation a, nw_function_definition def WHERE a.name = def.func_name
        UNION 
        SELECT DISTINCT a.id act_id, NULL, a.name func_name, a.line caller_line, a.caller_id 
        FROM nw.function_activation a WHERE NOT EXISTS
        (SELECT * FROM nw_function_definition def WHERE a.name = def.func_name);
        """
    cursor.executescript(view)

def nw_function_argument_variable():
    """
    nw_function_argument_variable(ActId, FuncName, LocalVarId, LocalVarName, Value, CallerVarId, CallerVarName) :-
        activation(_, ActId, FuncName, _,_,_,_),
        object_value(_, ActId, _, LocalVarName, _, 'ARGUMENT'),
        variable(_, ActId, LocalVarId, LocalVarName, _, Value, _),
        dependency(_,_, ActId, LocalVarId, CallerActivationId, CallerVarId),
        variable(_, CallerActivationId, CallerVarId, CallerVarName, _, Value,_).
    """
    view = """DROP TABLE IF EXISTS nw_function_argument_variable;
            CREATE TABLE nw_function_argument_variable AS
            SELECT DISTINCT a.id act_id, a.name func_name, v1.id local_var_id, v1.name local_var_name,
            v1.value value, v2.id caller_var_id, v2.name caller_var_name 
            FROM nw.function_activation a, nw.object_value val,
            nw.variable v1, nw.variable v2, nw.variable_dependency d 
            WHERE a.id = val.function_activation_id AND val.function_activation_id = v1.activation_id 
            AND val.name = v1.name AND v1.activation_id = d.source_activation_id 
            AND v1.id = d.source_id AND v2.activation_id = d.target_activation_id 
            AND v2.id = target_id AND v1.value = v2.value 
            AND val.type = 'ARGUMENT';
            """
    cursor.executescript(view)
    

def nw_function_argument_literal():
    """
        THIS IS A PIECE OF URGLY CODE IN MY SQLite IMPLEMENTATION.
    nw_function_argument_literal(ActId, FuncName, LocalVarId, LocalVarName, Value) :-
        activation(_, ActId, FuncName, _, _, _, _),
        object_value(_, ActId, _, LocalVarName, _, 'ARGUMENT'),
        variable(_, ActId, LocalVarId, LocalVarName, AssignmentLine, Value, _),
        nw_function_definition(_, FuncName, FuncDefLine, _, _),
        AssignmentLine = FuncDefLine,
        not nw_function_argument_variable(ActId, FuncName, _, LocalVarName, Value, _,_).
    """
    
    view = """
        DROP TABLE IF EXISTS nw_function_argument_literal;
        CREATE TABLE nw_function_argument_literal AS
        WITH temp1 AS (SELECT DISTINCT a.id act_id, a.name func_name,
        v.id local_var_id, v.name local_var_name, v.value value 
        FROM nw.function_activation a JOIN nw.object_value val 
        ON a.id = val.function_activation_id 
        JOIN nw.variable v ON val.function_activation_id = v.activation_id 
        JOIN nw_function_definition def 
        ON a.name = def.func_name AND def.first_line = v.line 
        WHERE val.type = 'ARGUMENT') 
        SELECT DISTINCT * FROM temp1 WHERE NOT EXISTS 
        (SELECT * FROM nw_function_argument_variable arg_v 
        WHERE arg_v.act_id = temp1.act_id AND arg_v.func_name = temp1.func_name 
        AND arg_v.local_var_name = temp1.local_var_name 
        AND arg_v.value = temp1.value);
        """
    cursor.executescript(view)

def nw_function_argument():
    """
    nw_function_argument(ActId, FuncName, LocalVarId, LocalVarName, Value, variable, CallerVarName, CallerVarId) :-
        nw_function_argument_variable(ActId, FuncName, LocalVarId, LocalVarName, Value, CallerVarId, CallerVarName),
        CallerVarId \== nil.
    nw_function_argument(ActId, FuncName, LocalVarId, LocalVarName, Value, literal, CallerVarName, CallerVarId) :-
        nw_function_argument_literal(ActId, FuncName, LocalVarId, LocalVarName, Value),
        CallerVarId = nil,
        CallerVarName = nil.
    """
    view = """DROP TABLE IF EXISTS nw_function_argument;
        CREATE TABLE nw_function_argument AS
        SELECT * FROM nw_function_argument_variable WHERE caller_var_id IS NOT NULL 
        UNION
        SELECT *, NULL,NULL FROM nw_function_argument_literal;
        
        """
    cursor.executescript(view)

def nw_variable_is_function():
    """
    nw_variable_is_function(VariableId) :-
        variable(_, VariableId, _, Name, Line, _, _),
        function_def(_,_, Name, _, Line, _,_).
    """
    view = """DROP TABLE IF EXISTS nw_variable_is_function;
        CREATE TABLE nw_variable_is_function AS
        SELECT DISTINCT v.activation_id variable_id 
        FROM nw.variable v, nw.function_def def 
        ON v.name = def.name AND v.line = def.first_line;
        """
    cursor.executescript(view)

def nw_variable_assignment():
    """
    nw_variable_assignment(ActId, VariableId, VariableName, Line, Value) :-
        variable(_, ActId, VariableId, VariableName, Line, Value, _),
        not nw_variable_is_function(VariableId),
        Line \== 0,
        VariableName \== 'return',
        Value \= 'now(n/a)'.
    """
    view = """DROP TABLE IF EXISTS nw_variable_assignment;
            CREATE TABLE nw_variable_assignment AS
            SELECT v.activation_id act_id, v.id variable_id, v.name variable_name, v.line, v.value variable_value
            FROM nw.variable v WHERE v.line != 0 AND v.name != 'return' 
            AND v.value != 'now(n/a)' AND NOT EXISTS 
            (SELECT * FROM nw_variable_is_function is_f WHERE is_f.variable_id = v.id);
            """
    cursor.executescript(view)

def nw_usage_is_function_call():
    """
    nw_usage_is_function_call(UsageId, VariableId) :-
        usage(_, _, VariableId, UsageId, Name, Line),
        activation(_,_, Name, Line, _,_,_).
    """
    view = """
        DROP TABLE IF EXISTS usage;
        CREATE TABLE usage AS
        SELECT u.trial_id, u.activation_id,
        u.variable_id, u.id, v.name, u.line 
        FROM nw.variable_usage u, nw.variable v 
        WHERE u.activation_id = v.activation_id AND u.variable_id = v.id;
        
        DROP TABLE IF EXISTS nw_usage_is_function_call;
        CREATE TABLE nw_usage_is_function_call AS
        SELECT DISTINCT u.id usage_id, u.Variable_Id variable_id
        FROM usage u, nw.function_activation a 
        WHERE u.line = a.line AND u.name = a.name;
        """
    cursor.executescript(view)

def nw_variable_usage():
    """
    nw_variable_usage(UsageId, ActId, VariableId, VariableName, VariableValue, Line) :-
        usage(_, ActId, VariableId, UsageId, VariableName, Line),
        variable(_,_, VariableId, VariableName, _, VariableValue, _),
        not nw_usage_is_function_call(UsageId, VariableId).
    """
    view = """DROP TABLE IF EXISTS nw_variable_usage;
        CREATE TABLE nw_variable_usage AS
        SELECT DISTINCT u.id usage_id, u.activation_id act_id, u.variable_id, u.name variable_name, v.value variable_value, u.line
        FROM usage u, nw.variable v WHERE u.variable_id = v.id 
        AND u.name = v.name AND NOT EXISTS 
        (SELECT * FROM nw_usage_is_function_call fc 
        WHERE fc.usage_id = u.id AND fc.variable_id = u.variable_id);
        """
    cursor.executescript(view)

def nw_variable_dependency():
    """
    nw_variable_dependency(Why, ActId, FuncName, AssignmentLine, DownstreamVarId, DownstreamVarName, UpstreamVarId, UpstreamVarName) :-
        dependency(_, _, ActId, DownstreamVarId, ActId, UpstreamVarId),
        nw_variable_assignment(ActId, DownstreamVarId, DownstreamVarName, AssignmentLine, _),
        nw_variable_usage(_, ActId, UpstreamVarId, UpstreamVarName, _, _),
        nw_function_activation(ActId, _, FuncName, _, _),
        Why = assignment.
    nw_variable_dependency(Why, CalledActId, FuncName, AssignmentLine, DownstreamVarId, DownstreamVarName, UpstreamVarId, UpstreamVarName) :-
        dependency(_, _, CalledActId, DownstreamVarId, CallerActId, UpstreamVarId),
        nw_variable_assignment(CalledActId, DownstreamVarId, DownstreamVarName, AssignmentLine, _),
        nw_variable_usage(_, _, UpstreamVarId, UpstreamVarName, _, _),
        nw_function_activation(CalledActId, _, FuncName, _, CallerActId),
        Why = argument.
    nw_variable_dependency(Why, CalledActId, FuncName, AssignmentLine, DownstreamVarId, DownstreamVarName, UpstreamVarId, UpstreamVarName) :-
        variable(_, CalledActId, UpstreamVarId, UpstreamVarName, _, _, _),
        variable(_, CalledActId, ReturnId, 'return', _, _, _),
        dependency(_, _, CalledActId, ReturnId, CalledActId, UpstreamVarId),
        variable(_, CallerActId, FunctionValueId, _, _, 'now(n/a)', _),
        dependency(_, _, CallerActId, FunctionValueId, CalledActId, ReturnId),
        variable(_, CallerActId, DownstreamVarId, DownstreamVarName, _, _, _),
        dependency(_, _, CallerActId, DownstreamVarId, CallerActId, FunctionValueId),
        nw_variable_assignment(_, DownstreamVarId, DownstreamVarName, AssignmentLine, _),
        nw_function_activation(CalledActId, _, FuncName, _, _),
        Why = return.
    """
    view = """DROP TABLE IF EXISTS nw_variable_dependency;
        CREATE TABLE nw_variable_dependency AS
        SELECT DISTINCT "assignment" AS "Why", d.source_activation_id act_id,
        a.func_name func_name, ass.line assignment_line, ass.variable_id downstream_var_id,
        ass.variable_name downstream_var_name, u.variable_id upstream_var_id, u.variable_name upstream_var_name
        FROM nw.variable_dependency d JOIN nw_variable_assignment ass 
        ON d.source_activation_id = d.target_activation_id 
        AND d.source_activation_id = ass.act_id AND d.source_id = ass.variable_id 
        JOIN nw_variable_usage u 
        ON ass.act_id = u.act_id AND d.target_id = u.variable_id 
        JOIN nw_function_activation a ON a.act_id = u.act_id
        UNION
        SELECT DISTINCT "argument" AS "WHY", d.source_activation_id act_id, 
        a.func_name func_name, ass.line assignment_line, ass.variable_id downstream_var_id, 
        ass.variable_name downstream_var_name, u.variable_id upstream_var_id, u.variable_name upstream_var_name
        FROM nw.variable_dependency d JOIN nw_variable_assignment ass 
        ON d.source_activation_id = ass.act_id AND d.source_id = ass.variable_id 
        JOIN nw_variable_usage u ON d.target_id = u.variable_id 
        JOIN nw_function_activation a ON a.act_id = ass.act_id AND a.caller_id = d.target_activation_id
        UNION
        SELECT DISTINCT "return" AS "Why", v1.activation_id act_id, a.func_name, 
        ass.line, ass.variable_id downstream_var_id, ass.variable_name downstream_var_name,
        v1.id upstream_var_id, v1.name upstream_var_name 
        FROM nw.variable v1, nw.variable v2, nw.variable v3, nw.variable v4, 
        nw.variable_dependency d1, nw.variable_dependency d2, nw.variable_dependency d3, 
        nw_variable_assignment ass, nw_function_activation a 
        WHERE v1.activation_id = v2.activation_id AND v2.activation_id = d1.source_activation_id 
        AND d1.source_activation_id = d1.target_activation_id AND v2.activation_id = d2.target_activation_id 
        AND v2.activation_id = a.act_id AND v1.id = d1.target_id AND v2.id = d1.source_id 
        AND v2.id = d2.target_id AND v3.id = d2.source_id AND v3.id = d3.target_id 
        AND v3.activation_id = d2.source_activation_id AND v3.activation_id = v4.activation_id 
        AND v3.activation_id = d3.source_activation_id AND v3.activation_id = d3.target_activation_id 
        AND v4.id = d3.source_id AND v4.id = ass.variable_id AND v4.name = ass.variable_name
        AND v2.name = 'return' AND v3.value = 'now(n/a)';
        """
    cursor.executescript(view)


def run_views():
    nw_script_activation()
    nw_function_definition()
    nw_function_activation()
    nw_function_argument_variable()
    nw_function_argument_literal()
    nw_function_argument()
    nw_variable_is_function()
    nw_variable_assignment()
    nw_usage_is_function_call()
    nw_variable_usage()
    nw_variable_dependency()

if __name__ == '__main__':
    
    connection = sqlite3.connect('nw_views.db')
    cursor = connection.cursor()
    cursor.execute("ATTACH 'nw_facts.db' as nw")
    
    run_views()
    
    cursor.execute("DETACH database nw")
    cursor.close()
    connection.close()