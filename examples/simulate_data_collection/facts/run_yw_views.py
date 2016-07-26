import sqlite3


def yw_source_file():
    view = """DROP TABLE IF EXISTS yw_source_file;
        CREATE TABLE yw_source_file AS
        SELECT * FROM yw.extractfacts_extract_source;
        """
    cursor.executescript(view)

def yw_parent_workflow():
    """
    yw_parent_workflow(ProgramId, WorkflowId, WorkflowName) :-
        has_subprogram(WorkflowId, ProgramId),
        program(WorkflowId, WorkflowName, _, _, _).
    yw_parent_workflow(ProgramId, nil, nil) :-
        not has_subprogram(_,ProgramId).
        """
    view = """DROP TABLE IF EXISTS yw_parent_workflow;
        CREATE TABLE yw_parent_workflow AS
        WITH top_level AS
        (SELECT program_id FROM yw.modelfacts_program
        EXCEPT SELECT subprogram_id FROM yw.modelfacts_has_subprogram)
        SELECT sub.subprogram_id program_id, sub.program_id workflow_id,
        p.program_name workflow_name
        FROM yw.modelfacts_has_subprogram sub NATURAL JOIN yw.modelfacts_program p
        UNION
        SELECT program_id, NULL, NULL FROM top_level;
        """
    cursor.executescript(view)

def yw_program():
    """
    yw_program(ProgramId, ProgramName, ParentWorkflowId, SourceId, BeginLine, EndLine) :-
        program(ProgramId, ProgramName, _, BeginId, EndId),
        annotation(BeginId, SourceId, BeginLine, _, _, _),
        annotation(EndId, SourceId, EndLine, _, _, _),
        yw_parent_workflow(ProgramId, ParentWorkflowId, _).
    """
    view = """DROP TABLE IF EXISTS yw_program;
        CREATE TABLE yw_program AS
        SELECT p.program_id, p.program_name, pw.workflow_id,
        a1.source_id, a1.line_number begin_line, a2.line_number end_line
        FROM yw.modelfacts_program p NATURAL JOIN yw_parent_workflow pw
        JOIN yw.extractfacts_annotation a1 JOIN yw.extractfacts_annotation a2
        WHERE p.begin_annotation_id = a1.annotation_id 
        AND p.end_annotation_id = a2.annotation_id 
        AND a1.source_id = a2.source_id;
    """
    cursor.executescript(view)


def yw_workflow():
    """
    yw_workflow(WorkflowId, WorkflowName, ParentWorkflowId, SourceId, BeginLine, EndLine) :-
        yw_program(WorkflowId, WorkflowName, ParentWorkflowId, SourceId, BeginLine, EndLine),
        workflow(WorkflowId).
    """
    view = """DROP TABLE IF EXISTS yw_workflow;
        CREATE TABLE yw_workflow AS
        SELECT p.* FROM yw_program p NATURAL JOIN yw.modelfacts_workflow;
        """
    cursor.executescript(view)


def yw_workflow_script():
    """
    yw_workflow_script(WorkflowId, WorkflowName, SourceId, SourceFile) :-
        yw_workflow(WorkflowId, WorkflowName, nil, SourceId,_,_),
        yw_source_file(SourceId, SourceFile).
    """
    view = """DROP TABLE IF EXISTS yw_workflow_script;
        CREATE TABLE yw_workflow_script AS
        SELECT program_id workflow_id, program_name workflow_name, source_id, source_path 
        FROM yw_workflow NATURAL JOIN yw_source_file;
    """
    cursor.executescript(view)

def yw_workflow_step():
    """
        yw_workflow_step(StepId, StepName, WorkflowId, SourceId, BeginLine, EndLine) :-
        yw_program(StepId, StepName, WorkflowId, SourceId, BeginLine, EndLine),
        not function(StepId),
        WorkflowId \== 'nil'.
        """
    view = """DROP TABLE IF EXISTS yw_workflow_step;
        CREATE TABLE yw_workflow_step AS
        SELECT p.* FROM yw_program p
        WHERE NOT EXISTS (SELECT * FROM yw.modelfacts_function)
        AND p.workflow_id IS NOT NULL;
    """
    cursor.executescript(view)

def yw_function():
    """
    yw_function(FunctionId, FunctionName, ParentWorkflowId, SourceId, BeginLine, EndLine) :-
        yw_program(FunctionId, FunctionName, ParentWorkflowId, SourceId, BeginLine, EndLine),
        function(FunctionId).
    """
    view = """DROP TABLE IF EXISTS yw_function;
        CREATE TABLE yw_function AS
        SELECT * FROM yw_program NATURAL JOIN yw.modelfacts_function;
    """
    cursor.executescript(view)


def yw_program_has_port():
    """
    yw_program_has_port(BlockId, PortId) :-
        has_in_port(BlockId, PortId).
    yw_program_has_port(BlockId, PortId) :-
        has_out_port(BlockId, PortId).
    """
    view = """DROP TABLE IF EXISTS yw_program_has_port;
        CREATE TABLE yw_program_has_port AS
        SELECT * FROM yw.modelfacts_has_in_port 
        UNION 
        SELECT * FROM yw.modelfacts_has_out_port;
    """
    cursor.executescript(view)

def yw_data():
    """
    yw_data(DataId, DataName, WorkflowId, WorkflowName) :-
        data(DataId, DataName, _),
        port(PortId, _, _, _, _, DataId),
        yw_program_has_port(ProgramId, PortId),
        yw_parent_workflow(ProgramId, WorkflowId, WorkflowName).
    """
    view = """DROP TABLE IF EXISTS yw_data;
        CREATE TABLE yw_data AS
        SELECT * FROM yw.modelfacts_has_in_port
        UNION
        SELECT * FROM yw.modelfacts_has_out_port;
    """
    cursor.executescript(view)

def _yw_input_port():
    """
    _yw_input_port(PortId, in, PortName, DataId) :-
        port(PortId, in, PortName, _, _, DataId).
    _yw_input_port(PortId, param, PortName, DataId) :-
        port(PortId, param, PortName, _, _, DataId).
    """
    view = """DROP TABLE IF EXISTS _yw_input_port;
        CREATE TABLE _yw_input_port AS
        SELECT port_id, port_type, port_name, data_id 
        FROM yw.modelfacts_port port WHERE port.port_type IN ('in', 'param');
    """
    cursor.executescript(view)

def yw_step_input():
    """
     yw_step_input(ProgramId, ProgramName, PortType, PortId, PortName, DataId, DataName) :-
        _yw_input_port(PortId, PortType, PortName, DataId),
        has_in_port(ProgramId, PortId),
        yw_program(ProgramId, ProgramName,_,_,_,_),
        data(DataId,DataName,_).
    """
    view = """DROP TABLE IF EXISTS yw_step_input;
        CREATE TABLE yw_step_input AS
        WITH _yw_input_port AS
        (SELECT port_type, port_id, port_name, data_id
        FROM yw.modelfacts_port port WHERE port.port_type IN ('in', 'param'))
        SELECT DISTINCT program_id, program_name, ip.*, data_name
        FROM _yw_input_port ip NATURAL JOIN yw.modelfacts_has_in_port hip 
        JOIN yw_program p ON hip.block_id = p.program_id NATURAL JOIN yw.modelfacts_data d;
    """
    cursor.executescript(view)

def yw_step_output():
    """
    yw_step_output(ProgramId, ProgramName, PortType, PortId, PortName, DataId, DataName) :-
        port(PortId, 'out', PortName, _, _, DataId),
        has_out_port(ProgramId, PortId),
        yw_program(ProgramId, ProgramName,_,_,_,_),
        data(DataId,DataName,_),
        PortType = out.
        """
    view = """DROP TABLE IF EXISTS yw_step_output;
        CREATE TABLE yw_step_output AS
        SELECT DISTINCT p.program_id, p.program_name, port.port_type, 
        port.port_id, port.port_name, d.data_id, d.data_name 
        FROM yw.modelfacts_port port NATURAL JOIN yw.modelfacts_has_out_port hop 
        JOIN yw_program p ON hop.block_id = p.program_id 
        NATURAL JOIN yw.modelfacts_data d WHERE port.port_type = 'out';
        """
    cursor.executescript(view)

def yw_inflow():
    """
    yw_inflow(WorkflowId, WorkflowName, StepInputDataId, StepInputDataName, StepId, StepName) :-
        yw_step_input(StepId, StepName, _, _, _, StepInputDataId, StepInputDataName),
        yw_step_input(WorkflowId, WorkflowName, _, _, _, _, StepInputDataName),
        yw_parent_workflow(StepId, WorkflowId, _),
        data(StepInputDataId, StepInputDataName, _).
        """
    view = """DROP TABLE IF EXISTS yw_inflow;
        CREATE TABLE yw_inflow AS
        SELECT in2.program_id workflow_id, in2.program_name workflow_name, 
        d.data_id step_input_data_id, d.data_name step_input_data_name, 
        in1.program_id step_id, in1.program_name step_name 
        FROM yw_step_input in1 NATURAL JOIN yw.modelfacts_data d 
        JOIN yw_step_input in2 ON in1.data_name = in2.data_name 
        JOIN yw_parent_workflow pw 
        ON in1.program_id = pw.program_id AND in2.program_id = pw.workflow_id;
        """
    cursor.executescript(view)

def yw_flow():
    """
    yw_flow(SourceProgramId, SourceProgramName, SourcePortId, SourcePortName, DataId, DataName, SinkPortId, SinkPortName, SinkProgramId, SinkProgramName) :-
        yw_step_output(SourceProgramId, SourceProgramName, _, SourcePortId, SourcePortName, DataId, DataName),
        yw_step_input(SinkProgramId, SinkProgramName, _, SinkPortId, SinkPortName, DataId, DataName).

        """
    view = """DROP TABLE IF EXISTS yw_flow;
        CREATE TABLE yw_flow AS
        SELECT output.program_id source_program_id, output.program_name source_program_name,
        output.port_id source_port_id, output.port_name source_port_name,
        output.data_id, output.data_name, input.port_id sink_port_id, input.port_name sink_port_name,
        input.program_id sink_program_id, input.program_name sink_program_name
        FROM yw_step_input input JOIN yw_step_output output ON input.data_id = output.data_id;
        """
    cursor.executescript(view)

def yw_outflow():
    """
    yw_outflow(StepId, StepName, StepOutDataId, StepOutDataName, WorkflowId, WorkflowName, WorkflowOutDataId, WorkflowOutDataName) :-
        yw_step_output(StepId, StepName, _, _, _, StepOutDataId, StepOutDataName),
        yw_step_output(WorkflowId, WorkflowName, _, _, _, WorkflowOutDataId, WorkflowOutDataName),
        WorkflowOutDataName = StepOutDataName,
        yw_parent_workflow(StepId, WorkflowId, _),
        data(StepOutDataId, StepOutDataName,_)
        """
    view = """DROP TABLE IF EXISTS yw_outflow;
        CREATE TABLE yw_outflow AS
        SELECT out1.program_id step_id, out1.program_name step_name, 
        d.data_id step_out_data_id, d.data_name step_out_data_name, 
        out2.program_id workflow_id, out2.program_name workflow_name, 
        out2.data_id workflow_out_data_id, out2.data_name workflow_out_data_name 
        FROM yw_step_output out1 NATURAL JOIN yw.modelfacts_data d 
        JOIN yw_step_output out2 ON out1.data_name = out2.data_name 
        JOIN yw_parent_workflow pw 
        ON out1.program_id = pw.program_id AND out2.program_id = pw.workflow_id;
        """
    cursor.executescript(view)

def yw_qualified_name():
    """
    yw_qualified_name(EntityType, Id, QualifiedName) :-
        program(Id, _, QualifiedName, _, _),
        EntityType = program.
    yw_qualified_name(EntityType, Id, QualifiedName) :-
        port(Id, _, _, QualifiedName, _, _),
        EntityType = port.
    yw_qualified_name(EntityType, Id, QualifiedName) :-
        data(Id, _, QualifiedName),
        EntityType = data.
        """
    view = """DROP TABLE IF EXISTS yw_qualified_name;
        CREATE TABLE yw_qualified_name AS
        SELECT 'program' AS 'entity_type', program_id id, 
        qualified_program_name qualified_name FROM yw.modelfacts_program 
        UNION 
        SELECT 'port' AS 'entity_type', port_id id, 
        qualified_port_name qualified_name FROM yw.modelfacts_port 
        UNION 
        SELECT 'data' AS 'entity_type', data_id id, 
        qualified_data_name qualified_name FROM yw.modelfacts_data;
        """
    cursor.executescript(view)

def yw_description():
    """
    yw_description(EntityType, Id, Name, Description) :-
        program(Id, Name, _, BeginAnnotationId, _),
        annotation_qualifies(DescAnnotationId, BeginAnnotationId),
        annotation(DescAnnotationId, _, _, 'desc', _, Description),
        EntityType = program.
    yw_description(EntityType, Id, Name, Description) :-
        port(Id, _, Name,_, PortAnnotationId, _),
        annotation_qualifies(DescAnnotationId, PortAnnotationId),
        annotation(DescAnnotationId, _, _, 'desc', _, Description),
        EntityType = port.
        """
    view = """DROP TABLE IF EXISTS yw_description;
        CREATE TABLE yw_description AS
        SELECT 'program' AS 'entity_type', p.program_id, p.program_name, a.value 
        FROM yw.modelfacts_program p, yw.extractfacts_annotation_qualifies aq, 
        yw.extractfacts_annotation a 
        WHERE p.begin_annotation_id = aq.primary_annotation_id 
        AND aq.qualifying_annotation_id = a.annotation_id AND a.tag = 'desc' 
        UNION 
        SELECT 'port' AS 'entity_type', po.port_id, po.port_name, a.value 
        FROM yw.modelfacts_port po, yw.extractfacts_annotation_qualifies aq, 
        yw.extractfacts_annotation a 
        WHERE po.port_annotation_id = aq.primary_annotation_id 
        AND aq.qualifying_annotation_id = a.annotation_id AND a.tag = 'desc';
        """
    cursor.executescript(view)


def run_views():
    yw_source_file()
    yw_parent_workflow()
    yw_program()
    yw_workflow()
    yw_workflow_script()
    yw_workflow_step()
    yw_function()
    yw_program_has_port()
    yw_data()
    yw_step_input()
    yw_step_output()
    yw_inflow()
    yw_flow()
    yw_outflow()
    yw_qualified_name()
    yw_description()


if __name__ == '__main__':
    
    connection = sqlite3.connect('yw_views.db')
    cursor = connection.cursor()
    cursor.execute("ATTACH '../csv/facts.db' as yw")
    
    run_views()
    
    cursor.execute("DETACH database yw")
    cursor.close()
    connection.close()