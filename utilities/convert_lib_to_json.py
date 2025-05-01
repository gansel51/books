import pandas as pd
import json

# Load Goodreads CSV
df = pd.read_csv("docs/assets/goodreads_library_export.csv")

# Filter rows where 'Bookshelves' contains 'nyc-collection'
filtered_df = df[df["Bookshelves"].str.contains("nyc-collection", na=False, case=False)]

# Drop rows with missing Title or Author
filtered_df = filtered_df.dropna(subset=["Title", "Author"])

# Combine and clean each entry
combined_entries = []
for _, row in filtered_df.iterrows():
    title = str(row["Title"]).replace("’", "'")
    author = str(row["Author"]).replace("’", "'").replace("             ", " ").replace("        ", " ")
    combined_entries.append(f"{title} by {author}")

# Sort the combined list alphabetically
combined_entries.sort()

# Export to books.json
with open("docs/assets/books.json", "w", encoding="utf-8") as f:
    json.dump(combined_entries, f, indent=2, ensure_ascii=False)

print(f"Exported {len(combined_entries)} entries to books.json.")
