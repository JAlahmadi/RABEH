# Main script, used to interface with user
import json
import os
from tkinter import Canvas
import pandas as pd
from matplotlib.patches import Rectangle
from Functions import *
import openai
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from tkinter import Tk, Canvas
import io
import PyPDF2
from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.text import Text

import textwrap
from datetime import date
from matplotlib import image as mpimg
from matplotlib import patches
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PyPDF2 import PdfMerger
import shutil




# ******* Initializing script *******
# ************** ******* ************
#openAIKey = os.getenv('openAI')
#AVKey = os.getenv('AVKey')
#AV_api_key = AVKey
#openai.api_key = openAIKey
AV_api_key = 'WXN32VQSZTFHZ1KK'
openai.api_key = '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'


print("Starting Financial document generator....")


# Taking stock ticker from User
#ticker = input("Please enter your requested Stock ticker : ")

def pdf(tic):
    ticker = tic

    # Step 1: Call get_stock_info function to call upon the Stock API

    meta_data = get_stock_info(ticker, AV_api_key)
    if(meta_data == {}):
        return -1
    cash_data = get_company_cash(ticker, AV_api_key)
    cash_position = extract_company_cash_position(cash_data)


    # Generating variables
    
    Name = meta_data['Name']
    Symbol = meta_data['Symbol']
    today = date.today()
    RGR = calculate_revenue_growth_rate(ticker,AV_api_key)
    DER = calculate_debt_to_equity_ratio(ticker,AV_api_key)
    GPM = calculate_gross_profit_margin(ticker,AV_api_key)
    ROE = calculate_roe(ticker,AV_api_key)
    CR = calculate_current_ratio(ticker,AV_api_key)
    QR = calculate_qr(ticker,AV_api_key)
    NPM = calculate_net_profit_margin(ticker,AV_api_key)
    #####################################################################################################
    ######################################## Generating PARAGRAPHES #####################################

    # Step 1: Generating the "Overview" Section.
    ############################################
    Overview = get_company_description(ticker, AV_api_key)

    # Use the Overview as the prompt for the GPT-3 API to generate a paraphrased response
    Overview_prompt = f"Summarize and paraphrase the following text in 100 to 110 words:\n{Overview}"
    Overview_API_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=Overview_prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    Overview_API_response = json.dumps(Overview_API_response)
    Overview_section = json.loads(Overview_API_response)["choices"][0]["text"]

    # Step 2 : Generating the "Growth" Section.
    ###########################################
    Growth_prompt = f"""You are now a security analyst tasked with providing a report on the growth and performance of {meta_data['Name']} ({meta_data['Symbol']}). Based on the following financial data, write a well-reasoned paragraph of 120 to 150 words that takes into account the company's performance in relation to broader economic trends:

- Market Capitalization: {meta_data['MarketCapitalization']}
- Earnings before interest, taxes, depreciation, and amortization (EBITDA): {meta_data['EBITDA']}
- Price-to-earnings (P/E) ratio: {meta_data['PERatio']}
- Price/earnings-to-growth ratio (PEG ratio): {meta_data['PEGRatio']}
- Book Value: {meta_data['BookValue']}
- Dividend Per Share: {meta_data['DividendPerShare']}
- Dividend Yield: {meta_data['DividendYield']}
- Earnings per share (EPS): {meta_data['EPS']}
- Revenue Per Share TTM: {meta_data['RevenuePerShareTTM']}
- Profit Margin: {meta_data['ProfitMargin']}
- Operating Margin TTM: {meta_data['OperatingMarginTTM']}
- Return On Assets TTM: {meta_data['ReturnOnAssetsTTM']}
- Return On Equity TTM: {meta_data['ReturnOnEquityTTM']}
- Revenue TTM: {meta_data['RevenueTTM']}
- Gross Profit TTM: {meta_data['GrossProfitTTM']}
- Diluted EPS TTM: {meta_data['DilutedEPSTTM']}
- Quarterly Earnings Growth YOY: {meta_data['QuarterlyEarningsGrowthYOY']}
- Quarterly Revenue Growth YOY: {meta_data['QuarterlyRevenueGrowthYOY']}"""

    Growth_API_response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=Growth_prompt,
    max_tokens=300,
    n=1,
    stop=None,
    temperature=0.7,
    )
    Growth_API_response = json.dumps(Growth_API_response)
    Growth_section = json.loads(Growth_API_response)["choices"][0]["text"]

    # Step 3 : Generating the  "Valuation Ratios" section
    #####################################################

    Ratios_prompt = f"""Please provide an analysis of the company's stock valuation based on the following financial metrics:

    - P/E Ratio: {meta_data['PERatio']}
    - Revenue Growth Rate: {RGR}
    - Debt-to-Equity Ratio: {DER}

    Please provide a well-reasoned text response of 110 to 150 words that takes into account the context of the industry and broader economic trends."""


    Ratios_API_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=Ratios_prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    Ratios_API_response = json.dumps(Ratios_API_response)
    Ratios_section = json.loads(Ratios_API_response)["choices"][0]["text"]

    # Step 4 : Generating the  "Financial Statment Analysis" section
    ################################################################

    financial_statment_prompt = Ratios_prompt = f"""Please provide a financial statement analysis for the company based on the following financial statements: 

    - Income Statement
    - Balance Sheet
    - Cash Flow Statement

    Please focus on the following key financial metrics and ratios:

    - Revenue Growth Rate: {RGR}
    - Gross Profit Margin: {GPM}
    - Net Profit Margin: {NPM}
    - Return on Equity (ROE): {ROE}
    - Debt-to-Equity Ratio (D/E Ratio): {DER}
    - Current Ratio: {CR}
    - Quick Ratio: {QR}

    Please provide a well-reasoned text response of 250 to 350 words that takes into account the context of the industry and broader economic trends."""

    financial_statment_API_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=financial_statment_prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    financial_statment_API_response = json.dumps(financial_statment_API_response)
    financial_statment_section = json.loads(financial_statment_API_response)["choices"][0]["text"]

    # Step 5 : Generating the  "Technical Analysis" section
    #######################################################
    """
    Ratios_prompt = (
        f"You are now a security analyist, using the data below, write me a paragraph between 120 and 150 words talking about the company's growth and performance: \n"
        f"- Symbol: {meta_data['Symbol']}\n"
        f"- Asset Type: {meta_data['AssetType']}"
    )

    Ratios_API_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=Ratios_prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    Ratios_API_response = json.dumps(Ratios_API_response)
    Ratios_section = json.loads(Ratios_API_response)["choices"][0]["text"]
    """

    ################################################################################################
    ######################################## Generating TABLES #####################################

    # Step 1: General information Table (df_1) Data frame
    df_1 = pd.DataFrame({
        'Exchange': [meta_data['Exchange']],
        'Sector': [meta_data['Sector']],
        'FiscalYearEnd': [meta_data['FiscalYearEnd']],
        'LatestQuarter': [meta_data['LatestQuarter']],
        'MarketCapitalization': [meta_data['MarketCapitalization']]
    })

    # Create the table 1
    table1_text = [df_1.columns] + df_1.values.tolist()

    # Step 2: Ratios and Shares Table (df_2) Data frame
    df_2 = pd.DataFrame({
        'EBITDA': [meta_data['EBITDA']],
        'PERatio': [meta_data['PERatio']],
        'PEGRatio': [meta_data['PEGRatio']],
        'BookValue': [meta_data['BookValue']],
        'DividendPerShare': [meta_data['DividendPerShare']],
        'DividendYield': [meta_data['DividendYield']],
        'EPS': [meta_data['EPS']]
    })

    # Create Table 2
    table2_text = [df_2.columns] + df_2.values.tolist()

    # Step 3: Trailing 12 months (TTM) - df_3 Data frame
    df_3 = pd.DataFrame({
        'RevenuePerShareTTM': [meta_data['RevenuePerShareTTM']],
        'ProfitMargin': [meta_data['ProfitMargin']],
        'ReturnOnAssetsTTM': [meta_data['ReturnOnAssetsTTM']],
        'ReturnOnEquityTTM': [meta_data['ReturnOnEquityTTM']],
        'RevenueTTM': [meta_data['RevenueTTM']],
        'GrossProfitTTM': [meta_data['GrossProfitTTM']]
    })

    # Create Table 3
    table3_text = [df_3.columns] + df_3.values.tolist()


    ################################################################################################
    ######################################## Generating CHARTS #####################################

    # Step 1: Generate a Undervalued or overvalued meter chart

    # Saving Chart as PNG


    

    # Step 2: Generate a Social media sentemental charts
    payload={}
    headers = {'Authorization': 'Token cfef832f2f72b2556e4d44ce9b70ae298d0673ac'}
    #To get the daily sentiment scores
    response = requests.request("GET", f'https://socialsentiment.io/api/v1/stocks/{Symbol}/sentiment/daily/', headers=headers, data=payload)
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



    # Step 3: Generate a Whale chart tool
    headers2 = {'accept': 'application/json',
    'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
    'Authorization': 'Token e44be8020cb415b5950f2c2a236c2b0c8fa77dfc'}
    r = requests.get(f"https://api.quiverquant.com/beta/historical/wallstreetbets/{Symbol}", headers=headers2)
    data2 = r.json()
    dates2 = [data_point['Date'] for data_point in data2]
    men = [data_point['Mentions'] for data_point in data2]
    # Saving Chart as PNG
    data = [go.Bar(x=dates2, y=men, name='Daily score',marker_color='red', width=5)]
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

    
    

    ####################################################################################################
    ######################################## Generating PDF PAGE 1 #####################################


    # Step 1: Define the function to generate a PDF document
    fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 Size
    # Add a rectangle patch to the figure
    border = patches.Rectangle((0, 0), 1, 1, linewidth=1, edgecolor='grey', facecolor='none', transform=ax.transAxes)
    ax.add_patch(border)
    ax.axis('tight')
    ax.axis('off')

    # Create Report title:
    plt.text(0.5, 0.82, f"{Name} ({Symbol}) ", transform=fig.transFigure, size=18, ha='center', color='grey')  # Text
    plt.text(0.5, 0.80, f'Updated on Date "{today}" ', transform=fig.transFigure, size=12, ha='center', color='grey', fontstyle='italic')  # Text

    # Display logo Yiazou Capital
    logo_img = mpimg.imread('ChatGPT_Logo.png') # Load the logo image

    # Display the logo image in the top left corner of the figure
    ax.imshow(logo_img, extent=[0.05, 0.198, 0.88, 0.98], aspect='auto')

    # Set the axes limits so that the logo image is not clipped
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Create Overview title and paragraph:
    limitedText = textwrap.wrap(Overview_section, width=100 )
    overViewMargin =  (len(limitedText) / 100)
    print (f" Overview Margin: {overViewMargin}")
    ax.text(0.12, 0.8, "Overview section:", size=9, ha='left')  # Text
    ax.text(0.12, 0.78 , f'\n'.join(limitedText), size=7, ha='left',va='top') # Text

    # Step 2: Creating tableS:
    # table formatter:
    def fixTableCells(table):
        for cell in table.get_children():
            cell.get_text().set_ha('left')

    # create table 1 (General info table) using matplotlib:

    table_1 = ax.table(cellText=table1_text, loc='center', bbox=[0.12, 0.635-overViewMargin, 0.75, 0.05]) # Table 1 Object
    fixTableCells(table_1)
    ax.text(0.12, 0.695-overViewMargin, "Table 1: Company overview", size=9, ha='left')  # Table 1 title

    # create table 2 (Ratios and Shares Table) using matplotlib:
    table_2 = ax.table(cellText=table2_text, loc='center', bbox=[0.12, 0.525-overViewMargin, 0.75, 0.05]) #Table 2 Object
    fixTableCells(table_2)
    ax.text(0.12, 0.585-overViewMargin, "Table 2: Ratios and Shares", size=9, ha='left')  # Table 1 title

    # create table 3 (Trailing 12 months (TTM)) using matplotlib:
    table_3 = ax.table(cellText=table3_text, loc='center', bbox=[0.12, 0.4-overViewMargin, 0.75, 0.05]) # Table 2 Object
    fixTableCells(table_3)
    ax.text(0.12, 0.47-overViewMargin, "Table 3: Trailing 12 months (TTM)", size=9,
            ha='left')  # Table 1 title

    # Create Growth section:

    limitedText2 = textwrap.wrap(Growth_section, width=100 )
    growthMargin =  (len(limitedText2) / 100)
    print (f" Growth margin: {growthMargin}")
    ax.text(0.12, 0.28, "Growth section:", size=9, ha='left')  # Text
    ax.text(0.12, 0.26 , f'\n'.join(limitedText2), size=7, ha='left',va='top') # Text

    # Saving PDF page 1

    pp = PdfPages(f"{Name}_Report_1.pdf")  # PDF Name
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
    #PDF_Name = f"{Name}_Report.pdf"
    PDF_Name_pg1 = f"{Name}_Report_1.pdf"

    ####################################################################################################
    ######################################## Generating PDF PAGE 2 #####################################

    fig2, ax2 = plt.subplots(figsize=(8.27, 11.69))  # A4 Size
    # Add a rectangle patch to the figure
    border2 = patches.Rectangle((0, 0), 1, 1, linewidth=1, edgecolor='grey', facecolor='none', transform=ax2.transAxes)
    ax2.add_patch(border2)
    ax2.axis('tight')
    ax2.axis('off')

    #  Page 2 title
    plt.text(0.5, 0.85, f"{Name} page 2 - continued ", transform=fig2.transFigure, size=10, ha='center', color='grey')  # Text


    # Create "Valuation Ratios" section title and paragraph:
    limitedText = textwrap.wrap(Ratios_section, width=100 )
    ValuationRatiosMargin =  (len(limitedText) / 100)
    print (f" Valuation Ratios Margin: {ValuationRatiosMargin}")
    ax2.text(0.12, 0.90, "Valuation Ratios section:", size=9, ha='left')  # Text
    ax2.text(0.12, 0.88 , f'\n'.join(limitedText), size=7, ha='left',va='top') # Text

    # paste "Valuation Ratios" png Charts


    # Create "Financial Statment" section title and paragraph:
    limitedText = textwrap.wrap(financial_statment_section, width=100 )
    FinancialStatmentMargin =  (len(limitedText) / 100)
    print (f" Financial Statment: {FinancialStatmentMargin}")
    ax2.text(0.11, 0.72, "Financial Statment section:", size=9, ha='left')  # Text
    ax2.text(0.11, 0.70 , f'\n'.join(limitedText), size=7, ha='left',va='top') # Text

    # paste "Sentimental analysis" png Chart

    # paste "Twitter trend chart" png Chart

    # Saving PDF page 2

    pp2 = PdfPages(f"{Name}_Report_2.pdf")  # PDF Name
    pp2.savefig(fig2, bbox_inches='tight')
    pp2.close()
    PDF_Name_pg2 = f"{Name}_Report_2.pdf"


    ###########################################################################################
    ######################################## END OF CODE  #####################################

    # Step 1: Merging pages
    merger = PdfMerger()

    merger.append(f"{Name}_Report_1.pdf")
    merger.append(f"{Name}_Report_2.pdf")
    merger.write(f"{Name}_Report.pdf")
    merger.close()

    print(f"Your report has been generated in the form of a PDF with the name {Name}_Report.pdf")
    print("Done")
    PDF_Name = f"{Name}_Report.pdf"
    shutil.move( f"{PDF_Name}", f'static/{PDF_Name}')
    return PDF_Name

