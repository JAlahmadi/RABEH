
import requests
from PyPDF2 import PdfMerger
import img2pdf
import plotly.graph_objs as go
import plotly.io as pio
import plotly.express as px
ss_api_key = "cfef832f2f72b2556e4d44ce9b70ae298d0673ac"
#Set the URL of the API endpoint and the headers
url = "https://api.quiverquant.com/beta/historical/wallstreetbets/AAPL"
headers = {'accept': 'application/json',
'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
'Authorization': 'Token e44be8020cb415b5950f2c2a236c2b0c8fa77dfc'}
r = requests.get(url, headers=headers)
data = r.json()
#print(r.content)
dates = [data_point['Date'] for data_point in data]
men = [data_point['Mentions'] for data_point in data]

# Generate plotly chart
data = [go.Bar(x=dates, y=men, name='Daily score',marker_color='red', width=5)]
layout = go.Layout(height=300, width=500)
fig = go.Figure(data=data, layout=layout)
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
chart_image = pio.to_image(fig, format='png')

# Save chart image
with open('wallBets.png', 'wb') as f:
    f.write(chart_image)
from PIL import Image

# Load the generated image
image = Image.open("wallBets.png")

# Define the region to crop
left = 37
top = 87
right = 633
bottom = 242

# Crop the image
cropped_image = image.crop((left, top, right, bottom))

# Save the cropped image
cropped_image.save("wallBets.png")





#=========================================chart 1===========================================================================
payload={}
headers = {'Authorization': 'Token cfef832f2f72b2556e4d44ce9b70ae298d0673ac'}
#To get the daily sentiment scores
response = requests.request("GET", url+f'https://socialsentiment.io/api/v1/stocks/{Symbol}/sentiment/daily/', headers=headers, data=payload)
#Parse the JSON responses using the built-in json library.
data = response.json()
# Saving Chart as PNG
import plotly.graph_objs as go
import plotly.io as pio

dates = [data_point['date'] for data_point in data]
scores = [data_point['score'] for data_point in data]
avg_7_days = [data_point['avg_7_days'] for data_point in data]
avg_14_days = [data_point['avg_14_days'] for data_point in data]
avg_30_days = [data_point['avg_30_days'] for data_point in data]

# Generate plotly chart
data = [go.Bar(x=dates, y=scores, name='Daily score'), go.Bar(x=dates, y=avg_7_days, name='7-day moving average'), go.Bar(x=dates, y=avg_14_days, name='14-day moving average'),
        go.Bar(x=dates, y=avg_30_days, name='30-day moving average')]
layout = go.Layout(title='Daily Sentiment Score & 7 Day Moving Average')
fig = go.Figure(data=data, layout=layout)
chart_image = pio.to_image(fig, format='png')

# Save chart image
with open('Sentiment_Score.png', 'wb') as f:
    f.write(chart_image)
#==============================================================chart 2===================================================

# Step 3: Generate a Whale chart tool
url = f"https://api.quiverquant.com/beta/historical/wallstreetbets/{Symbol}"
headers = {'accept': 'application/json',
'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
'Authorization': 'Token e44be8020cb415b5950f2c2a236c2b0c8fa77dfc'}
r = requests.get(url, headers=headers)
data = r.json()
#print(r.content)
dates = [data_point['Date'] for data_point in data]
men = [data_point['Mentions'] for data_point in data]
# Saving Chart as PNG
data = [go.Bar(x=dates, y=men, name='Daily score',marker_color='red', width=5)]
layout = go.Layout(height=300)
fig = go.Figure(data=data, layout=layout)
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
chart_image = pio.to_image(fig, format='png')

# Save chart image
with open('wallBets.png', 'wb') as f:
    f.write(chart_image)
from PIL import Image

# Load the generated image
image = Image.open("wallBets.png")

# Define the region to crop
left = 37
top = 87
right = 633
bottom = 242

# Crop the image
cropped_image = image.crop((left, top, right, bottom))

# Save the cropped image
cropped_image.save("wallBets.png")
