# 📊 VizAgent: AI-Powered Web Analytics Dashboarding System

**VizAgent** is an LLM-powered, modular agentic system that transforms raw web analytics CSVs into executive-ready dashboards with zero manual effort.

---

## 🚀 Features

- 🧼 **Automated Cleaning**  
  Handles nulls, duplicate rows, stringified numbers, and more

- 📊 **Exploratory Data Analysis (EDA)**  
  Generates visual reports using Sweetviz and YData-Profiling

- 🤖 **Visualization Planner**  
  GPT-4-based dashboard planning: recommends charts, dimensions, filters

- 📤 **Tableau Export**  
  Converts cleaned data into `.hyper` files and outputs a dashboard plan JSON

- 💡 **Streamlit Interface**  
  Drag-and-drop CSV upload, interactive previews, downloadable reports

---

## 🧠 Architecture

Each step is handled by a dedicated agent following the **One Agent, One Task** principle:

| Agent                  | Role                                                                 |
|------------------------|----------------------------------------------------------------------|
| Ingestion Agent        | Validates CSV and extracts schema                                    |
| Cleaning Agent         | Cleans data using PyJanitor and DuckDB fallback                     |
| EDA Agent              | Produces profiling reports and LLM-generated insights                |
| Visualization Agent    | Calls GPT to generate chart specs and storytelling                  |
| Export Agent           | Outputs `.hyper` and chart spec JSON for Tableau                    |

---

## 🛠️ Stack

- **Python 3.10+**
- **Streamlit** for UI
- **OpenAI GPT-4 / 3.5** via `openai` API
- **Pantab + Tableau Hyper API** for data export
- **YData-Profiling**, **Sweetviz**, **PyJanitor**
- **DuckDB**, **Polars** (fallbacks for big files)

---

## 📂 Sample Output

- `vizagent_output.hyper` → Tableau-compatible data extract
- `dashboard_plan.json` → Chart specs (chart type, dimensions, measures, filter, story)
- Downloadable EDA reports (`.html`)

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/yourusername/vizagent.git
cd vizagent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
decativate
python3 -m venv eda_env
source eda_env/bin/activate
pip install -r eda_requirements.txt
deactivate
source venv/bin/activate
streamlit run app/streamlit_app.py
```

Add your OpenAI key in .env

---

## 📈 Use Cases
- Web Traffic Analysis
- Conversion funnel tracking
- Campaign performance reporting
- Lightweight BI without manual dashboarding

---
