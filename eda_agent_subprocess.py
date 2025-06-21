import pandas as pd
import sweetviz
from ydata_profiling import ProfileReport
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: python eda_agent_subprocess.py <input_csv> <output_dir>")
        return
    input_path = sys.argv[1]
    output_dir = sys.argv[2]

    df = pd.read_csv(input_path)

    ydata_path = os.path.join(output_dir, "ydata_profile.html")
    sweetviz_path = os.path.join(output_dir, "sweetviz_report.html")

    print(" Generating YData profile...")
    profile = ProfileReport(df, title="YData Report", explorative=True)
    profile.to_file(ydata_path)

    print("Generating Sweetviz report...")
    report = sweetviz.analyze(df)
    report.show_html(sweetviz_path, open_browser=False)

    print("✅ EDA Complete")
    print(f"YData profile saved to: {ydata_path}")
    print(f"Sweetviz report saved to: {sweetviz_path}")
    print("🎉 EDA reports generated successfully!")

if __name__ == "__main__":
    main()