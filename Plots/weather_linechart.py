import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')

# Array for each month
months = ["July", "August", "September", "October", "November", "December",
          "January", "February", "March", "April", "May", "June"]

# Empty data frame to collect each max value
final_df = pd.DataFrame()

for x in months:
    # Filtering month
    filtered_df = df[df['month'] == x]

    # Sorting values and select top temp
    new_df = filtered_df.sort_values(by=['actual_max_temp'], ascending=[False]).head(31)

    final_df = final_df.append(new_df.iloc[[0]])

# Preparing data
data = [go.Scatter(x=final_df['month'], y=final_df['actual_max_temp'], mode='lines', name='Temp')]

# Preparing layout
layout = go.Layout(title='Weather for July 2014 - June 2015', xaxis_title="Month",
                   yaxis_title="Max temp (F)")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='weather_linechart.html')