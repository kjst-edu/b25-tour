from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir/"demo.csv")

for col in ['a', 'b', 'c', 'd']:
    df[col] = pd.to_numeric(df[col], errors='coerce')