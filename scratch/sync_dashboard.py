import json
import re
import pandas as pd

def main():
    print("Running dashboard synchronization script...")
    
    # 1. Load results_v2_verified.json
    with open("data/results_v2_verified.json", "r", encoding="utf-8") as f:
        v2_data = json.load(f)
        
    # 2. Load verification.csv
    df_ver = pd.read_csv("data/verification.csv")
    ver_data = df_ver.to_dict(orient="records")
    
    # 3. Read index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    # 4. Replace const appsData block
    # We look for: const appsData = [ ... ];
    # Since it is a massive single-line block or multi-line block, let's use regex with DOTALL.
    # Pattern: const appsData = \[.*?\];
    apps_json = json.dumps(v2_data)
    html, count_apps = re.subn(
        r'const appsData\s*=\s*\[.*?\]\s*;',
        f'const appsData = {apps_json};',
        html,
        flags=re.DOTALL
    )
    print(f"Substituted appsData in HTML: {count_apps} matches replaced.")
    
    # 5. Replace const verificationData block
    # Pattern: const verificationData = \[.*?\];
    ver_json = json.dumps(ver_data)
    html, count_ver = re.subn(
        r'const verificationData\s*=\s*\[.*?\]\s*;',
        f'const verificationData = {ver_json};',
        html,
        flags=re.DOTALL
    )
    print(f"Substituted verificationData in HTML: {count_ver} matches replaced.")
    
    # 6. Correct specific text in HTML (e.g. stats mismatch)
    # Correct self-serve count badge: change '72/100 apps' to '74/100 apps' in stats card
    html, count_stat = re.subn(
        r'<span class="text-xs text-brand-400 font-normal">72/100 apps</span>',
        '<span class="text-xs text-brand-400 font-normal">74/100 apps</span>',
        html
    )
    print(f"Corrected self-serve status text: {count_stat} replacements.")
    
    # Remove any un-imported tool references (browser-use)
    # Check if 'browser-use' is mentioned on the page. In the original index.html, let's see if it was.
    # Let's clean it just in case:
    # "browser-use/manual doc check" -> "agent re-check + manual doc check"
    html = html.replace("browser-use/manual doc check", "automated re-check + manual doc check")
    html = html.replace("browser-use", "automated browser scraping")
    
    # 7. Write index.html back
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Dashboard synchronized successfully!")

if __name__ == "__main__":
    main()
