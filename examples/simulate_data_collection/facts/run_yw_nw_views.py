import sqlite3

def nw_activation_from_yw_step():
    """
    nw_activation_from_yw_step(ActivationId, FunctionName, StepId, StepName, ActivationLine) :-
        nw_function_activation(ActivationId, _, FunctionName, ActivationLine, _),
        yw_workflow_step(StepId, StepName, _, _,  StepBeginLine, StepEndLine),
        line_inside_range(ActivationLine, StepBeginLine, StepEndLine).
    """
    view = """DROP TABLE IF EXISTS nw_activation_from_yw_step;
            CREATE TABLE nw_activation_from_yw_step AS
            SELECT DISTINCT na.act_id, na.func_name, ys.program_id step_id, ys.program_name step_name, na.caller_line act_line
            FROM yw.yw_workflow_step ys, nw.nw_function_activation na 
            WHERE na.caller_line >= ys.begin_line AND na.caller_line <= ys.end_line;
            """
    cursor.executescript(view)


def nw_activation_into_yw_program():
    """
    nw_activation_into_yw_program(ActivationId, FunctionName, StepId, StepName, ActivationLine, CallerActivationId) :-
        yw_program(StepId, StepName, _, _,  StepBeginLine, StepEndLine),
        nw_function_activation(ActivationId, _, FunctionName, ActivationLine, CallerActivationId),
        line_outside_range(ActivationLine, StepBeginLine, StepEndLine),
        nw_function_definition(_, FunctionName, FunctionStartLine, _, _),
        line_inside_range(FunctionStartLine, StepBeginLine, StepEndLine).
    """
    view = """DROP TABLE IF EXISTS nw_activation_into_yw_program;
            CREATE TABLE nw_activation_into_yw_program AS
            SELECT DISTINCT na.act_id, na.func_name, yp.program_id step_id, 
            yp.program_name step_name, na.caller_line, na.caller_id 
            FROM yw.yw_program yp, nw.nw_function_activation na, 
            nw.nw_function_definition nd 
            WHERE (na.caller_line < yp.begin_line OR na.caller_line > yp.end_line) 
            AND na.func_name = nd.func_name 
            AND nd.first_line >= yp.begin_line AND nd.first_line <= yp.end_line;
            """
    cursor.executescript(view)


def nw_activation_into_yw_step_subprogram():
    """
    nw_activation_into_yw_step_subprogram(ActivationId, StepId) :-
        nw_activation_into_yw_program(ActivationId, _, StepId, _, _, _),
        nw_activation_into_yw_program(ActivationId, _, SubprogramId, _, _, _),
        yw_workflow_step(SubprogramId, _, StepId, _, _, _).
    """
    view = """DROP TABLE IF EXISTS nw_activation_into_yw_step_subprogram;
            CREATE TABLE nw_activation_into_yw_step_subprogram AS
            SELECT aip1.act_id, aip1.step_id FROM nw_activation_into_yw_program aip1,
            nw_activation_into_yw_program aip2, yw.yw_workflow_step ys 
            WHERE aip1.act_id = aip2.act_id AND ys.program_id = aip2.step_id 
            AND ys.workflow_id = aip1.step_id;
    """
    cursor.executescript(view)

def nw_activation_into_yw_step():
    """
    nw_activation_into_yw_step(ActivationId, FunctionName, StepId, StepName, ActivationLine, CallerActivationId) :-
        nw_activation_into_yw_program(ActivationId, FunctionName, StepId, StepName, ActivationLine, CallerActivationId),
        not nw_activation_into_yw_step_subprogram(ActivationId, StepId).
        """
    view = """DROP TABLE IF EXISTS nw_activation_into_yw_step;
        CREATE TABLE nw_activation_into_yw_step AS
        SELECT * FROM nw_activation_into_yw_program program 
        WHERE NOT EXISTS 
        (SELECT * FROM nw_activation_into_yw_step_subprogram subprogram 
        WHERE subprogram.act_id = program.act_id AND subprogram.step_id = program.step_id);
        """
    cursor.executescript(view)

def nw_variable_for_yw_in_port_10():
    """
    nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, Type, PortId, PortName, StepId, StepName) :-
        nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName),
        Type = variable.
    nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, Type, PortId, PortName, StepId, StepName) :-
        nw_argument_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName),
        Type = argument.
    nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, Type, PortId, PortName, StepId, StepName) :-
        nw_variable_for_yw_inflow(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName),
        Type = inflow.
    nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, Type, PortId, PortName, StepId, StepName) :-
        nw_variable_for_yw_in_port_defined(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName),
        Type = defined.
        """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_in_port_10;
        CREATE TABLE nw_variable_for_yw_in_port_10 AS
        SELECT *, 'variable' AS 'type' FROM nw_variable_for_yw_in_port_9
        UNION
        SELECT *, 'argument' AS 'type' FROM nw_argument_for_yw_in_port
        UNION
        SELECT *, 'inflow' AS 'type' FROM nw_variable_for_yw_inflow
        UNION
        SELECT *, 'defined' AS 'type' FROM nw_variable_for_yw_in_port_defined;
        """
    cursor.executescript(view)

def nw_variable_for_yw_out_port():
    """
    nw_variable_for_yw_out_port(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        nw_variable_for_yw_out_port_assigned(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName).
    nw_variable_for_yw_out_port(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        nw_variable_for_yw_out_port_thru(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName).
    nw_variable_for_yw_out_port(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        nw_variable_for_yw_outflow(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName).
        """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_out_port;
        CREATE TABLE nw_variable_for_yw_out_port AS
        SELECT * FROM nw_variable_for_yw_out_port_assigned
        UNION
        SELECT * FROM nw_variable_for_yw_out_port_thru
        UNION
        SELECT * FROM nw_variable_for_yw_outflow;
        """
    cursor.executescript(view)

def nw_variable_for_yw_data():
    """
    nw_variable_for_yw_data(VariableId, VariableName, VariableValue, DataId, DataName) :-
        nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, _, _, _, _, _).
    nw_variable_for_yw_data(VariableId, VariableName, VariableValue, DataId, DataName) :-
        nw_variable_for_yw_out_port(VariableId, VariableName, VariableValue, DataId, DataName, _, _, _, _).
    """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_data;
        CREATE TABLE nw_variable_for_yw_data AS
        SELECT variable_id,variable_name,variable_value,data_id,data_name 
        FROM nw_variable_for_yw_in_port_10
        UNION
        SELECT variable_id,variable_name,variable_value,data_id,data_name
        FROM nw_variable_for_yw_out_port;
        """
    cursor.executescript(view)

def nw_variable_assigned_in_yw_step():
    """
    nw_variable_assigned_in_yw_step(VariableId, VariableName, VariableValue, StepId, StepName, AssignmentLine) :-
        yw_workflow_step(StepId, StepName,_,_, StepBeginLine, StepEndLine),
        nw_variable_assignment(_, VariableId, VariableName, AssignmentLine, VariableValue),
        line_inside_range(AssignmentLine, StepBeginLine, StepEndLine).
        """
    view = """DROP TABLE IF EXISTS nw_variable_assigned_in_yw_step;
        CREATE TABLE nw_variable_assigned_in_yw_step AS
        SELECT DISTINCT na.variable_id, na.variable_name, na.variable_value,
        ys.program_id step_id, ys.program_name step_name, na.line 
        FROM yw.yw_workflow_step ys, nw.nw_variable_assignment na 
        WHERE na.line >= ys.begin_line AND na.line <= ys.end_line;
        """
    cursor.executescript(view)

def nw_variable_assigned_outside_yw_step():
    """
    nw_variable_assigned_outside_yw_step(VariableId, VariableName, VariableValue, StepId, StepName, AssignmentLine) :-
        yw_workflow_step(StepId, StepName,_,_, StepBeginLine, StepEndLine),
        nw_variable_assignment(_, VariableId, VariableName, AssignmentLine, VariableValue),
        line_outside_range(AssignmentLine, StepBeginLine, StepEndLine).
        """
    view = """DROP TABLE IF EXISTS nw_variable_assigned_outside_yw_step;
        CREATE TABLE nw_variable_assigned_outside_yw_step AS
        SELECT DISTINCT na.variable_id, na.variable_name, na.variable_value,
        ys.program_id step_id, ys.program_name step_name, na.line 
        FROM yw.yw_workflow_step ys, nw.nw_variable_assignment na 
        WHERE na.line < ys.begin_line OR na.line > ys.end_line;
        """
    cursor.executescript(view)

def nw_variable_used_in_yw_step():
    """
    nw_variable_used_in_yw_step(VariableId, VariableName, VariableValue, StepId, StepName, UsageLine) :-
        yw_workflow_step(StepId, StepName,_,_, StepBeginLine, StepEndLine),
        nw_variable_usage(_, _, VariableId, VariableName, VariableValue, UsageLine),
        line_inside_range(UsageLine, StepBeginLine, StepEndLine).
        """
    view = """DROP TABLE IF EXISTS nw_variable_used_in_yw_step;
        CREATE TABLE nw_variable_used_in_yw_step AS
        SELECT DISTINCT nu.variable_id, nu.variable_name, nu.variable_value,
        ys.program_id step_id, ys.program_name step_name, nu.line
        FROM yw.yw_workflow_step ys, nw.nw_variable_usage nu
        WHERE nu.line >= ys.begin_line AND nu.line <= ys.end_line;
        """
    cursor.executescript(view)

def nw_variable_used_outside_yw_step():
    """
    nw_variable_used_outside_yw_step(VariableId, VariableName, VariableValue, StepId, StepName, UsageLine) :-
        yw_workflow_step(StepId, StepName,_,_, StepBeginLine, StepEndLine),
        nw_variable_usage(_, _, VariableId, VariableName, VariableValue, UsageLine),
        line_outside_range(UsageLine, StepBeginLine, StepEndLine).
        """
    view = """DROP TABLE IF EXISTS nw_variable_used_outside_yw_step;
        CREATE TABLE nw_variable_used_outside_yw_step AS
        SELECT DISTINCT nu.variable_id, nu.variable_name, nu.variable_value,
        ys.program_id step_id, ys.program_name step_name, nu.line
        FROM yw.yw_workflow_step ys, nw.nw_variable_usage nu
        WHERE nu.line < ys.begin_line OR nu.line > ys.end_line;
        """
    cursor.executescript(view)

def nw_variable_for_yw_in_port_9():
    """
        nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        PortName = VariableName,
        yw_step_input(StepId, StepName, _, PortId, PortName, DataId, DataName),
        nw_variable_used_in_yw_step(VariableId, VariableName, VariableValue, StepId, _, _),
        nw_variable_assigned_outside_yw_step(VariableId, _, _, StepId, _, _).
        """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_in_port_9;
        CREATE TABLE nw_variable_for_yw_in_port_9 AS
        SELECT DISTINCT uis.variable_id, uis.variable_name, uis.variable_value, yi.data_id,
        yi.data_name, yi.port_id, yi.port_name, yi.program_id step_id, yi.program_name step_name
        FROM yw.yw_step_input yi, nw_variable_used_in_yw_step uis,
        nw_variable_assigned_outside_yw_step aos
        WHERE uis.step_id = yi.program_id AND yi.port_name = uis.variable_name
        AND uis.variable_id = aos.variable_id AND uis.step_id = aos.step_id;
        """
    cursor.executescript(view)

def nw_argument_for_yw_in_port():
    """
    nw_argument_for_yw_in_port(VarId, VarName, VarValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        yi:yw_step_input(StepId, StepName, _, PortId, PortName, DataId, DataName),
        yp:yw_program(StepId, _, _, _, StepBeginLine, StepEndLine),
        VarName = PortName,
        na:nw_function_argument(ActId, _, VarId, _, _, _, _, _),
        
        nass:nw_variable_assignment(ActId, VarId, VarName, AssignmentLine, VarValue),
        line_inside_range(AssignmentLine, StepBeginLine, StepEndLine),
        
        not nw_variable_for_yw_in_port(VarId, _, _, _, _, PortId, _, _, _),
        nact:nw_function_activation(ActId, _, _, CallLine, _),
        line_outside_range(CallLine, StepBeginLine, StepEndLine).
        """
    view = """DROP TABLE IF EXISTS nw_argument_for_yw_in_port;
        CREATE TABLE nw_argument_for_yw_in_port AS
        SELECT DISTINCT nass.variable_id, nass.variable_name, nass.variable_value, yi.data_id, 
        yi.data_name, yi.port_id, yi.port_name, yi.program_id step_id, yi.program_name step_name 
        FROM yw.yw_step_input yi, yw.yw_program yp, nw.nw_function_argument na, 
        nw.nw_variable_assignment nass, nw.nw_function_activation nact 
        WHERE yi.program_id = yp.program_id AND na.act_id = nass.act_id 
        AND na.local_var_id = nass.variable_id AND nass.variable_name = yi.port_name 
        AND nass.line >= yp.begin_line AND nass.line <= yp.end_line 
        AND NOT EXISTS (SELECT * FROM nw_variable_for_yw_in_port_9 vip 
        WHERE vip.variable_id = na.local_var_id AND vip.port_id = yi.port_id) 
        AND nact.act_id = na.act_id 
        AND (nact.caller_line < yp.begin_line OR nact.caller_line > yp.end_line);
        """
    cursor.executescript(view)

def nw_variable_for_yw_in_port_defined():
    """
    nw_variable_for_yw_in_port_defined(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        PortName = VariableName,
        yw_step_input(StepId, StepName, _, PortId, PortName, DataId, DataName),
        nw_variable_assigned_in_yw_step(VariableId, VariableName, VariableValue, StepId, _, _),
        not nw_variable_assigned_outside_yw_step(_, VariableName, _, StepId, _, _),
        not nw_argument_for_yw_in_port(_, VariableName, _, _, _, _, _, StepId, _).
        """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_in_port_defined;
        CREATE TABLE nw_variable_for_yw_in_port_defined AS
        SELECT DISTINCT  ais.variable_id,  ais.variable_name,  ais.variable_value, yi.data_id, yi.data_name,
        yi.port_id, yi.port_name, yi.program_id step_id, yi.program_name step_name 
        FROM yw.yw_step_input yi, nw_variable_assigned_in_yw_step  ais 
        WHERE yi.port_name =  ais.variable_name AND yi.program_id =  ais.step_id 
        AND NOT EXISTS (SELECT * FROM nw_variable_assigned_outside_yw_step  aos, 
        nw_argument_for_yw_in_port aip 
        WHERE  aos.variable_name = aip.variable_name AND  aos.step_id = aip.step_id 
        AND  aos.variable_name =  ais.variable_name AND  aos.step_id =  ais.step_id);
        """
    cursor.executescript(view)

def nw_variable_for_yw_inflow():
    """
    nw_variable_for_yw_inflow(VariableId, VariableName, VariableValue, WorkflowInDataId, WorkflowInDataName, WorkflowPortId, WorkflowPortName, WorkflowId, WorkflowName) :-
        nw_argument_for_yw_in_port(VariableId, VariableName, VariableValue, StepInDataId, StepInDataName, _, _, StepId, StepName),
        yw_inflow(WorkflowId, WorkflowName, StepInDataId, StepInDataName, StepId, StepName),
        WorkflowInDataName = StepInDataName,
        yw_step_input(WorkflowId, WorkflowName, _, WorkflowPortId, WorkflowPortName, WorkflowInDataId, WorkflowInDataName).
        """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_inflow;
        CREATE TABLE nw_variable_for_yw_inflow AS
        SELECT aip.variable_id, aip.variable_name, aip.variable_value, yi.data_id workflow_id_data_id, 
        yi.data_name workflow_in_data_name, yi.port_id workflow_port_id, yi.port_name workflow_port_name, 
        yi.program_id workflow_id, yi.program_name workflow_name 
        FROM nw_argument_for_yw_in_port aip, yw.yw_inflow inflow, yw.yw_step_input yi 
        WHERE aip.data_id = inflow.step_input_data_id AND aip.data_name = inflow.step_input_data_name 
        AND aip.step_id = inflow.step_id AND aip.step_name = inflow.step_name
        AND inflow.step_input_data_name = yi.data_name 
        AND inflow.workflow_id = yi.program_id AND inflow.workflow_name = yi.program_name;
        """
    cursor.executescript(view)

def nw_variable_for_yw_out_port_assigned():
    """
    nw_variable_for_yw_out_port_assigned(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        yw_step_output(StepId, _, _, PortId, PortName, DataId, DataName),
        PortName = VariableName,
        nw_variable_assigned_in_yw_step(VariableId, VariableName, VariableValue, StepId, StepName, _),
        nw_variable_used_outside_yw_step(VariableId, _, _, StepId, _, _).
        """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_out_port_assigned;
        CREATE TABLE nw_variable_for_yw_out_port_assigned AS
        SELECT ais.variable_id, ais.variable_name, ais.variable_value, yo.data_id, yo.data_name, 
        yo.port_id, yo.port_name, ais.step_id, ais.step_name 
        FROM yw.yw_step_output yo, nw_variable_assigned_in_yw_step ais, 
        nw_variable_used_outside_yw_step uos 
        WHERE yo.port_name = ais.variable_name AND yo.program_id = ais.step_id 
        AND ais.variable_id = uos.variable_id AND ais.step_id = uos.step_id;
        """
    cursor.executescript(view)

def nw_variable_for_yw_out_port_thru():
    """
    nw_variable_for_yw_out_port_thru(VariableId, VariableName, VariableValue, DataId, DataName, PortId, PortName, StepId, StepName) :-
        PortName = VariableName,
        yw_step_output(StepId, StepName, _, PortId, PortName, DataId, DataName),
        nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, _, _, _, _, _, StepId, _),
        not nw_variable_assigned_in_yw_step(_, VariableName, _, StepId, _, _).
        """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_out_port_thru;
        CREATE TABLE nw_variable_for_yw_out_port_thru AS
        SELECT vip.variable_id, vip.variable_name, vip.variable_value, yo.data_id, yo.data_name, 
        yo.port_id, yo.port_name, yo.program_id step_id, yo.program_name step_name 
        FROM yw.yw_step_output yo, nw_variable_for_yw_in_port_9 vip 
        WHERE yo.port_name = vip.variable_name AND yo.program_id = vip.step_id 
        AND NOT EXISTS (SELECT * FROM nw_variable_assigned_in_yw_step ais 
        WHERE yo.port_name = vip.variable_name = ais.variable_name AND vip.step_id = ais.step_id);
        """
    cursor.executescript(view)

def nw_variable_for_yw_outflow():
    """
    nw_variable_for_yw_outflow(VariableId, VariableName, VariableValue, WorkflowOutDataId, WorkflowOutDataName, WorkflowPortId, WorkflowPortName, WorkflowId, WorkflowName) :-
        nw_variable_for_yw_out_port_thru(VariableId, VariableName, VariableValue, StepOutDataId, StepOutDataName, _, _, StepId, _),
        WorkflowOutDataName = StepOutDataName,
        yw_outflow(StepId, _, StepOutDataId, StepOutDataName, WorkflowId, WorkflowName, WorkflowOutDataId, WorkflowOutDataName),
        yw_step_output(WorkflowId, _, out, WorkflowPortId, WorkflowPortName, WorkflowOutDataId, _).
    """
    view = """DROP TABLE IF EXISTS nw_variable_for_yw_outflow;
        CREATE TABLE nw_variable_for_yw_outflow AS
        SELECT thru.variable_id, thru.variable_name, thru.variable_value, 
        outflow.workflow_out_data_id, outflow.workflow_out_data_name, 
        yo.port_id workflow_port_id, yo.port_name workflow_port_name, 
        outflow.workflow_id, outflow.workflow_name 
        FROM nw_variable_for_yw_out_port_thru thru, yw.yw_outflow outflow, yw.yw_step_output yo 
        WHERE thru.data_id = outflow.step_out_data_id AND thru.data_name = outflow.step_out_data_name 
        AND outflow.step_out_data_name = outflow.workflow_out_data_name 
        AND thru.step_id = outflow.step_id AND outflow.workflow_id = yo.program_id 
        AND outflow.workflow_out_data_id = yo.data_id AND yo.port_type = 'out';
        """
    cursor.executescript(view)




def run_views():
    nw_activation_from_yw_step()
    nw_activation_into_yw_program()
    nw_activation_into_yw_step_subprogram()
    nw_activation_into_yw_step()
    run_rules()
    nw_variable_for_yw_in_port_10()
    nw_variable_for_yw_out_port()
    nw_variable_for_yw_data()

def run_rules():
    nw_variable_assigned_in_yw_step()
    nw_variable_assigned_outside_yw_step()
    nw_variable_used_in_yw_step()
    nw_variable_used_outside_yw_step()
    nw_variable_for_yw_in_port_9()
    nw_argument_for_yw_in_port()
    nw_variable_for_yw_in_port_defined()
    nw_variable_for_yw_inflow()
    nw_variable_for_yw_out_port_assigned()
    nw_variable_for_yw_out_port_thru()
    nw_variable_for_yw_outflow()



if __name__ == '__main__':
    
    connection = sqlite3.connect('yw_nw_views.db')
    cursor = connection.cursor()
    cursor.execute("ATTACH 'nw_views.db' as nw")
    cursor.execute("ATTACH 'yw_views.db' as yw")
    
    run_views()
    
    cursor.execute("DETACH database nw")
    cursor.execute("DETACH database yw")
    cursor.close()
    connection.close()