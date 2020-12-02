import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv("../Datasets/Weather2014-15.csv")

# Array for each month
months = ["July", "August", "September", "October", "November", "December",
          "January", "February", "March", "April", "May", "June"]

final_max_df = pd.DataFrame()
final_min_df = pd.DataFrame()
final_mean_df = pd.DataFrame()

for x in months:
    # Filtering month
    filtered_df = df[df['month'] == x]

    # Sorting values and select max average temp
    new_df = filtered_df.sort_values(by=['average_max_temp'], ascending=[False]).head(31)

    final_max_df = final_max_df.append(new_df.iloc[[0]])

    # Sorting values and select min average temp
    new_df = filtered_df.sort_values(by=['average_min_temp'], ascending=[True]).head(31)

    final_min_df = final_min_df.append(new_df.iloc[[0]])

# Preparing data
data = [
    go.Scatter(x=final_min_df["average_min_temp"],
               y=final_max_df["average_max_temp"],
               text=final_min_df["month"],
               mode="markers",
               marker=dict(size=final_max_df["average_max_temp"],
                           color=final_max_df["average_max_temp"], showscale=True))
]

# Preparing layout

layout = go.Layout(title="Weather for July 2014 - June 2015", xaxis_title="Min Tempterature (F)",
                   yaxis_title="Max Temperature (F)", hovermode="closest")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename="weather_bubblechart.html")