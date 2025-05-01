import json

import pandas as pd


df = pd.read_excel("docs/assets/nyc-collection.xlsx")

# Clean and convert all titles to strings
titles = df["Title"].dropna().astype(str)

# Sort titles alphabetically
titles = sorted(titles)

# Save to JSON
with open("docs/assets/books.json", "w") as f:
    json.dump(titles, f, indent=2)