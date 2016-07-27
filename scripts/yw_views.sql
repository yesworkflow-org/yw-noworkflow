ATTACH 'facts/yw_facts.db' as yw;

DROP TABLE IF EXISTS yw_source_file;
CREATE TABLE yw_source_file AS
        SELECT * FROM yw.extractfacts_extract_source;

DROP TABLE IF EXISTS yw_parent_workflow;
CREATE TABLE yw_parent_workflow AS
        WITH top_level AS
        (SELECT program_id FROM yw.modelfacts_program
        EXCEPT SELECT subprogram_id FROM yw.modelfacts_has_subprogram)
        SELECT sub.subprogram_id program_id, sub.program_id workflow_id,
        p.program_name workflow_name
        FROM yw.modelfacts_has_subprogram sub NATURAL JOIN yw.modelfacts_program p
        UNION
        SELECT program_id, NULL, NULL FROM top_level;

DROP TABLE IF EXISTS yw_program;
CREATE TABLE yw_program AS
        SELECT p.program_id, p.program_name, pw.workflow_id,
        a1.source_id, a1.line_number begin_line, a2.line_number end_line
        FROM yw.modelfacts_program p NATURAL JOIN yw_parent_workflow pw
        JOIN yw.extractfacts_annotation a1 JOIN yw.extractfacts_annotation a2
        WHERE p.begin_annotation_id = a1.annotation_id 
        AND p.end_annotation_id = a2.annotation_id 
        AND a1.source_id = a2.source_id;

DROP TABLE IF EXISTS yw_workflow;
CREATE TABLE yw_workflow AS
        SELECT p.* FROM yw_program p NATURAL JOIN yw.modelfacts_workflow;

DROP TABLE IF EXISTS yw_workflow_script;
CREATE TABLE yw_workflow_script AS
        SELECT program_id workflow_id, program_name workflow_name, source_id, source_path 
        FROM yw_workflow NATURAL JOIN yw_source_file;

DROP TABLE IF EXISTS yw_workflow_step;
CREATE TABLE yw_workflow_step AS
        SELECT p.* FROM yw_program p
        WHERE NOT EXISTS (SELECT * FROM yw.modelfacts_function)
        AND p.workflow_id IS NOT NULL;

DROP TABLE IF EXISTS yw_function;
CREATE TABLE yw_function AS
        SELECT * FROM yw_program NATURAL JOIN yw.modelfacts_function;

DROP TABLE IF EXISTS yw_program_has_port;
CREATE TABLE yw_program_has_port AS
        SELECT * FROM yw.modelfacts_has_in_port 
        UNION 
        SELECT * FROM yw.modelfacts_has_out_port;

DROP TABLE IF EXISTS yw_data;
CREATE TABLE yw_data AS
        SELECT * FROM yw.modelfacts_has_in_port
        UNION
        SELECT * FROM yw.modelfacts_has_out_port;

DROP TABLE IF EXISTS _yw_input_port;
CREATE TABLE _yw_input_port AS
        SELECT port_id, port_type, port_name, data_id 
        FROM yw.modelfacts_port port WHERE port.port_type IN ('in', 'param');

DROP TABLE IF EXISTS yw_step_input;
CREATE TABLE yw_step_input AS
        WITH _yw_input_port AS
        (SELECT port_type, port_id, port_name, data_id
        FROM yw.modelfacts_port port WHERE port.port_type IN ('in', 'param'))
        SELECT DISTINCT program_id, program_name, ip.*, data_name
        FROM _yw_input_port ip NATURAL JOIN yw.modelfacts_has_in_port hip 
        JOIN yw_program p ON hip.block_id = p.program_id NATURAL JOIN yw.modelfacts_data d;

DROP TABLE IF EXISTS yw_step_output;
CREATE TABLE yw_step_output AS
        SELECT DISTINCT p.program_id, p.program_name, port.port_type, 
        port.port_id, port.port_name, d.data_id, d.data_name 
        FROM yw.modelfacts_port port NATURAL JOIN yw.modelfacts_has_out_port hop 
        JOIN yw_program p ON hop.block_id = p.program_id 
        NATURAL JOIN yw.modelfacts_data d WHERE port.port_type = 'out';

DROP TABLE IF EXISTS yw_inflow;
CREATE TABLE yw_inflow AS
        SELECT in2.program_id workflow_id, in2.program_name workflow_name, 
        d.data_id step_input_data_id, d.data_name step_input_data_name, 
        in1.program_id step_id, in1.program_name step_name 
        FROM yw_step_input in1 NATURAL JOIN yw.modelfacts_data d 
        JOIN yw_step_input in2 ON in1.data_name = in2.data_name 
        JOIN yw_parent_workflow pw 
        ON in1.program_id = pw.program_id AND in2.program_id = pw.workflow_id;

DROP TABLE IF EXISTS yw_flow;
CREATE TABLE yw_flow AS
        SELECT output.program_id source_program_id, output.program_name source_program_name,
        output.port_id source_port_id, output.port_name source_port_name,
        output.data_id, output.data_name, input.port_id sink_port_id, input.port_name sink_port_name,
        input.program_id sink_program_id, input.program_name sink_program_name
        FROM yw_step_input input JOIN yw_step_output output ON input.data_id = output.data_id;

DROP TABLE IF EXISTS yw_outflow;
CREATE TABLE yw_outflow AS
        SELECT out1.program_id step_id, out1.program_name step_name, 
        d.data_id step_out_data_id, d.data_name step_out_data_name, 
        out2.program_id workflow_id, out2.program_name workflow_name, 
        out2.data_id workflow_out_data_id, out2.data_name workflow_out_data_name 
        FROM yw_step_output out1 NATURAL JOIN yw.modelfacts_data d 
        JOIN yw_step_output out2 ON out1.data_name = out2.data_name 
        JOIN yw_parent_workflow pw 
        ON out1.program_id = pw.program_id AND out2.program_id = pw.workflow_id;

DROP TABLE IF EXISTS yw_qualified_name;
CREATE TABLE yw_qualified_name AS
        SELECT 'program' AS 'entity_type', program_id id, 
        qualified_program_name qualified_name FROM yw.modelfacts_program 
        UNION 
        SELECT 'port' AS 'entity_type', port_id id, 
        qualified_port_name qualified_name FROM yw.modelfacts_port 
        UNION 
        SELECT 'data' AS 'entity_type', data_id id, 
        qualified_data_name qualified_name FROM yw.modelfacts_data;

DROP TABLE IF EXISTS yw_description;
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


DETACH database yw;