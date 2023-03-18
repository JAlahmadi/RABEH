
import requests
from PyPDF2 import PdfMerger
import img2pdf
ss_api_key = "cfef832f2f72b2556e4d44ce9b70ae298d0673ac"
#Set the URL of the API endpoint and the headers
url = 'https://socialsentiment.io/api/v1'
payload={}
headers = {'Authorization': 'Token cfef832f2f72b2556e4d44ce9b70ae298d0673ac'}
#To get the daily sentiment scores
params = {'symbol': 'AAPL', 'from': '2022-03-10', 'to': '2022-03-16'}
response = requests.request("GET", url+'/stocks/AAPL/sentiment/daily/', headers=headers, data=payload)
#To get the 7-day moving average,
response_avg = requests.request("GET", url+'/stocks/AAPL/sentiment/now/', headers=headers, data=payload)
#Parse the JSON responses using the built-in json library.
data = response.json()
data_avg = response_avg.json()
print(data)
print('=======================================================')
print(data_avg)
#Extract the daily sentiment scores and the moving average from the JSON data.
#scores = [item['score'] for item in data[0]['sentiment']]
#moving_avg = [item['score'] for item in data_avg['sentiment_avg']]
#Plot the daily sentiment scores and the moving average using a Python plotting library such as matplotlib or seaborn.
#================================================
import plotly.graph_objs as go
import plotly.io as pio
from PyPDF2 import PdfFileMerger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
with open('chart.png', 'wb') as f:
    f.write(chart_image)

# Generate PDF
c = canvas.Canvas('my_pdf.pdf', pagesize=letter)
c.drawString(100, 750, "Hello world")
c.save()
ccc = canvas.Canvas('my_pdf2.pdf', pagesize=letter)
ccc.drawString(100, 750, "Hello world")
ccc.save()

with open("my_pdf2.pdf","wb") as f:
	f.write(img2pdf.convert('chart.png'))

# Merge PDF with chart image
merger = PdfMerger()
merger.append(open('my_pdf.pdf', 'rb'))
merger.append(open('my_pdf2.pdf', 'rb'))
merger.write('merged_pdf.pdf')
merger.close()



#================================
'''import plotly.graph_objs as go

# Extract data
dates = [data_point['date'] for data_point in data]
scores = [data_point['score'] for data_point in data]
avg_7_days = [data_point['avg_7_days'] for data_point in data]
avg_14_days = [data_point['avg_14_days'] for data_point in data]
avg_30_days = [data_point['avg_30_days'] for data_point in data]

# Create traces
score_trace = go.Scatter(x=dates, y=scores, name='Daily score')
avg_7_trace = go.Scatter(x=dates, y=avg_7_days, name='7-day moving average')
avg_14_trace = go.Scatter(x=dates, y=avg_14_days, name='14-day moving average')
avg_30_trace = go.Scatter(x=dates, y=avg_30_days, name='30-day moving average')

# Create layout
layout = go.Layout(title='Daily sentiment scores and moving averages for AAPL')

# Create figure
fig = go.Figure(data=[score_trace, avg_7_trace, avg_14_trace, avg_30_trace], layout=layout)

# Show plot
fig.show()'''



#This code uses the datetime module to convert the date strings in the list of dictionaries to datetime objects, then creates two separate lists for the dates and scores. It then calculates the 7-day moving average and creates a line graph using the matplotlib library.

#Note that in the moving_avg_list, the first six entries are None because there are not enough previous days to calculate a 7-day moving average. This is why the if i < 6 condition is included in the loop.

