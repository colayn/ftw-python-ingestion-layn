import pandas as pd
import yaml

# Set the directory path
path = "/projects/ftw-python-ingestion/data/test"

# --- CSV ---
print("\n=== CSV ===")
df_csv = pd.read_csv(f"{path}.csv")
print(df_csv)

# --- TSV ---
print("\n=== TSV ===")
df_tsv = pd.read_csv(f"{path}.tsv", sep="\t")
print(df_tsv)

# --- JSON ---
print("\n=== JSON ===")
df_json = pd.read_json(f"{path}.json")
print(df_json)

# --- XML ---
print("\n=== XML ===")
df_xml = pd.read_xml(f"{path}.xml")
print(df_xml)

# --- YAML ---
print("\n=== YAML ===")
with open(f"{path}.yml", "r") as file:
    yaml_data = yaml.safe_load(file)
df_yaml = pd.DataFrame(yaml_data)
print(df_yaml)

# --- HTML ---
print("\n=== HTML ===")
df_html = pd.read_html(f"{path}.html")[0]
print(df_html)

df_html.to_csv("output/flat_example.csv",index=False)