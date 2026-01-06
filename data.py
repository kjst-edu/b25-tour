from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir/"not demo.csv")

for col in ["治安指数","衛生指数","国際評価指数","気候指数"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')