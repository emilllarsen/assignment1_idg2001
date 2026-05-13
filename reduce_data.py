"""Script to reduce the Olympic dataset to post-1994 entries."""
import pandas as pd

df = pd.read_csv("app/data/athlete_events.csv")
df = df[df["Year"] >= 1994]
df.to_csv("app/data/athlete_events.csv", index=False)
print(f"Reduced to {len(df)} rows")