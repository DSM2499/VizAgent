import pandas as pd
import pantab
import os
import json
from datetime import datetime

def export_hyper(df: pd.DataFrame, output_dir = "outputs/generated_dashboards/") -> str:
    os.makedirs(output_dir, exist_ok = True)
    hyper_path = os.path.join(output_dir, "vizagent_output.hyper")
    pantab.frame_to_hyper(df, hyper_path, table = "Extract")
    return hyper_path

def export_chart_plan_json(plan_text: str, output_dir = "outputs/generated_dashboards/") -> str:
    os.makedirs(output_dir, exist_ok = True)
    json_path = os.path.join(output_dir, "dashboard_plan.json")

    try:
        if isinstance(plan_text, str):
            parsed = json.loads(plan_text)
        else:
            parsed = plan_text
        with open(json_path, "w") as f:
            json.dump(parsed, f, indent = 2)
        return json_path
    except Exception as e:
        return f"Error: {str(e)}"