from preswald import (connect, get_df, query, select, slider, text, table, plotly)
import plotly.express as px

# 1. Connected and loaded
connect()
df = get_df("world_happiness_report")
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Renamed common columns
for old in ("country_or_region", "country_name"):
    if old in df.columns:
        df = df.rename(columns={old: "country"})
if "score" in df.columns and "happiness_score" not in df.columns:
    df = df.rename(columns={"score": "happiness_score"})

# 2. UI widgets
countries = sorted(df["country"].unique())
chosen = select("🌍 Pick a country", options=countries, default=countries[0])

yr_min, yr_max = int(df["year"].min()), int(df["year"].max())
start, end = slider("Year range", min=yr_min, max=yr_max,
                    value=(yr_min, yr_max), step=1)

# 3. SQL filter
sql = f"""
SELECT *
FROM world_happiness_report
WHERE LOWER(REPLACE(Country, ' ', '_')) = '{chosen.lower().replace(' ', '_')}'
  AND Year BETWEEN {start} AND {end}
ORDER BY Year
"""
filtered = query(sql, "world_happiness_report")

# 4. Output
text(f"# 🙂 {chosen}: Happiness {start}-{end}")
table(filtered, title="Raw data")

fig = px.line(filtered,
              x="Year",
              y="Happiness_Score",
              title=f"Happiness Score over time – {chosen}",
              markers=True)
plotly(fig)

avg_sql = f"""
SELECT Year, AVG(Happiness_Score) AS avg_score
FROM world_happiness_report
WHERE Year BETWEEN {start} AND {end}
GROUP BY Year
ORDER BY Year
"""
avg_df = query(avg_sql, "world_happiness_report")

fig_avg = px.bar(avg_df,
                 x="Year",
                 y="avg_score",
                 title="🌍 Global Average Happiness Score by Year")
plotly(fig_avg)



#from preswald import connect, get_df, select, slider, text, table, plotly
#import plotly.express as px

#connect()
#df = get_df("world_happiness_report")

#df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns:
#
#for old in ("country_or_region", "country_name"):
#    if old in df.columns:
#        df = df.rename(columns={old: "country"})
#if "score" in df.columns and "happiness_score" not in df.columns:
#    df = df.rename(columns={"score": "happiness_score"})

#countries = sorted(df["country"].unique())
#chosen = select("🌍 Pick a country", options=countries, default=countries[0])

#yr_min, yr_max = int(df["year"].min()), int(df["year"].max())
#start, end = slider("Year range",
#                    min=yr_min, max=yr_max
#                    value=(yr_min, yr_max), step=1)
#                    
#filtered = (
#    df[(df["country"] == chosen) &
#    (df["year"].between(start, end))]
#    .sort_values("year")
#)
#
#text(f"#😀{chosen}: Happiness {start}-{end}")
#table(filtered, title="Raw data")
#
#fig = px.line(filtered
#            x="year",
#            y="happiness_score",
#            title=f"Happiness Score over time - {chosen}",
#            markers=True)
#plotly(fig)