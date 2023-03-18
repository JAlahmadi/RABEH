import requests
import openai
import pyaudio
import wave
openai.api_key = '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'

#################################################################################################
######################################## Overview functions #####################################
def get_stock_info(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    return data



def get_company_description(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    return data['Description']


#################################################################################################
######################################## Cashflow functions #####################################

def get_company_cash(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    return data


def extract_company_cash_position(data):
    # get the latest annual report
    latest_report = data['annualReports'][0]

    # extract the desired cash flow items from the latest report
    operating_cashflow = int(latest_report['operatingCashflow'])
    cashflow_from_investment = int(latest_report['cashflowFromInvestment'])
    cashflow_from_financing = int(latest_report['cashflowFromFinancing'])
    cash_position = str(operating_cashflow + cashflow_from_investment + cashflow_from_financing)    # return the extracted data as a tuple
    return cash_position





##############################################################################################
######################################## Ratio functions #####################################

def calculate_debt_to_equity_ratio(symbol, api_key):
    # Define Alpha Vantage API endpoint and parameters
    # Make API request to get balance sheet data
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    balance_sheet = response.json()

    # Get the required data points to calculate debt-to-equity ratio
    total_liabilities = float(balance_sheet["annualReports"][0]["totalLiabilities"])
    total_shareholder_equity = float(balance_sheet["annualReports"][0]["totalShareholderEquity"])

    # Calculate debt-to-equity ratio
    debt_to_equity_ratio = total_liabilities / total_shareholder_equity
    debt_to_equity_ratio = round(debt_to_equity_ratio, 2)
    return debt_to_equity_ratio


def calculate_revenue_growth_rate(symbol, api_key):
    # Define Alpha Vantage API endpoint and parameters
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'INCOME_STATEMENT',
        'symbol': symbol,
        'apikey': api_key
    }

    # Send request to Alpha Vantage API
    response = requests.get(url, params=params)

    # Extract revenue data from response
    income_statements = response.json()['annualReports']
    revenues = [float(stmt['totalRevenue']) for stmt in income_statements]

    # Calculate revenue growth rate
    current_revenue = revenues[0]
    previous_revenue = revenues[1]
    revenue_growth_rate = ((current_revenue - previous_revenue) / previous_revenue) * 100

    # Return revenue growth rate
    revenue_growth_rate = round(revenue_growth_rate, 2)
    return revenue_growth_rate

def calculate_gross_profit_margin(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    gross_profit = float(data['annualReports'][0]['grossProfit'])
    total_revenue = float(data['annualReports'][0]['totalRevenue'])
    gross_profit_margin = gross_profit / total_revenue
    gross_profit_margin = round(gross_profit_margin, 2)
    return gross_profit_margin


def calculate_roe(symbol, api_key):
    # Get data from income statement
    url_income_statement = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}"
    response_income_statement = requests.get(url_income_statement)
    data_income_statement = response_income_statement.json()
    print('hh')
    print(data_income_statement)
    # Get data from balance sheet
    url_balance_sheet = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}"
    response_balance_sheet = requests.get(url_balance_sheet)
    data_balance_sheet = response_balance_sheet.json()
    print(data_income_statement)
    # Calculate net income
    net_income = float(data_income_statement["annualReports"][0]['netIncome'])

    # Calculate average shareholders' equity
    total_shareholder_equity = float(data_balance_sheet['annualReports'][0]['totalShareholderEquity'])
    total_shareholder_equity_prev = float(data_balance_sheet['annualReports'][1]['totalShareholderEquity'])
    average_shareholder_equity = (total_shareholder_equity + total_shareholder_equity_prev) / 2

    # Calculate return on equity (ROE)
    roe = net_income / average_shareholder_equity
    roe = round(roe, 2)
    return roe


def calculate_current_ratio(symbol, api_key):
    # make request to Alpha Vantage API for balance sheet data
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # extract relevant data points
    total_current_assets = float(data["annualReports"][0]["totalCurrentAssets"])
    total_current_liabilities = float(data["annualReports"][0]["totalCurrentLiabilities"])

    # calculate current ratio
    current_ratio = total_current_assets / total_current_liabilities
    current_ratio = round(current_ratio, 2)
    return current_ratio


def calculate_qr(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    cash_and_equivalents = float(data['annualReports'][0]['cashAndCashEquivalentsAtCarryingValue'])
    short_term_investments = float(data['annualReports'][0]['shortTermInvestments'])
    print(data['annualReports'][0]['currentNetReceivables'])
    accounts_receivable = float(data['annualReports'][0]['currentNetReceivables'])
    current_liabilities = float(data['annualReports'][0]['totalCurrentLiabilities'])
    quick_ratio = (cash_and_equivalents + short_term_investments + accounts_receivable) / current_liabilities
    return round(quick_ratio, 2)



def calculate_net_profit_margin(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    net_income = float(data['annualReports'][0]['netIncome'])
    total_revenue = float(data['annualReports'][0]['totalRevenue'])
    net_profit_margin = (net_income / total_revenue) * 100
    return round(net_profit_margin, 2)


def recorder():
    frames_buf = 3200
    format = pyaudio.paInt16
    CHANNELS =1
    RATE = 16000

    p= pyaudio.PyAudio()

    stream = p.open(
        format= format,
        channels= CHANNELS,
        rate= RATE,
        input= True,
        frames_per_buffer= frames_buf
    )

    print("start recording ....")

    sec = 6
    frames =[]
    for i in range(0, int(RATE/frames_buf*sec)):
        data = stream.read(frames_buf)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate
    print("end recording")
    obj = wave.open("output.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(format))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close()

def audio_transcript():
    audio_file= open('output.wav', 'rb')
    transcript = openai.Audio.translate(
        model= 'whisper-1',
        file=audio_file,
        response_format= 'text'
        )
    print(transcript)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": transcript},
        {"role": "user", "content": "can you get the company stock ticker? only write the ticker"}
    ]
    )
    print(completion.choices[-1].message.content)
    return completion.choices[-1].message.content

