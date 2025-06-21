import json
from xml.etree.ElementTree import Element, SubElement, tostring
import os
from xml.dom import minidom

def prettify(elm):
    return minidom.parseString(tostring(elm)).toprettyxml(indent = "  ")

def create_twb_from_plan(hyper_file_name: str, dashboard_json_path: str, output_path = "outputs/workbooks/vizagent_dashboard.twb"):
    os.makedirs(os.path.dirname(output_path), exist_ok = True)

    with open(dashboard_json_path, "r") as f:
        plan = json.load(f)
    
    root = Element("workbook")
    root.set("version", "21.1")
    root.set("source-build", "VizAgent")
    root.set("source-version", "21.1")
    root.set("has-user-views", "false")

    ds = SubElement(root, "datasources")
    datasource = SubElement(ds, "datasource")
    datasource.set("name", "VizAgentSource")
    datasource.set("hasextract", "true")
    SubElement(datasource, "connection").set("class", "hyper")
    SubElement(datasource, "extract").set("file", hyper_file_name)

    worksheets = SubElement(root, "worksheets")

    for i, chart in enumerate(plan["dashboard_plan"]["charts"]):
        ws = SubElement(worksheets, "worksheet")
        ws.set("name", f"Chart {i + 1}")
        ws_desc = SubElement(ws, "description")
        ws_desc.text = chart["story"]

        #Note: We are not rendering actual charts - this is a shell
    
    os.makedirs(os.path.dirname(output_path), exist_ok = True)
    with open(output_path, "w") as f:
        f.write(prettify(root))
    return output_path