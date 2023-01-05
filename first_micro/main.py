from flask import Flask, render_template, request, url_for
from markupsafe import escape # to escape user inputs and so avoid injection attacks
import requests
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import base64
from io import BytesIO


app = Flask(__name__)

prefix_google="""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-STW104EH1L"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-STW104EH1L');
    </script>
    """
user_input=""

@app.route('/', methods=["GET"])
def hello_world():
    title="<h1>Hello</h1>"
    details="<p>You are analyzed by Google Analytics</p>"
    button=f"<a href='{url_for('click')}'>click here</a><br>"
    button+=f"<a href='{url_for('logger')}'>see logs</a>"
    display=prefix_google+title+details+button
    return display

@app.route('/click', methods=["GET"])
def click():
    return prefix_google+"You have clicked"

@app.route('/logger', methods=["GET", "POST"])
def logger():
    global user_input
    print('This is a log from python')
    if request.method == 'POST':
        user_input+=escape(request.form.get("user_input"))
        user_input+='\n'
    else:
        user_input+='\n'
    
    return prefix_google+render_template('logger.html', text=user_input)


if __name__ == "__main__":
    app.run(debug=True)

@app.route('/cookie', methods = ["GET", "POST"])
def cookie():
    req = requests.get("https://www.google.com/")

    return req.cookies.get_dict()

@app.route('/GA', methods = ["GET", "POST"])
def cookieGA():
    req = requests.get("https://analytics.google.com/analytics/web/#/p345095181/reports/intelligenthome?params=_u..nav%3Dmaui")

    return req.text

# @app.route('/visitors', methods = ["GET", "POST"])
# def get_visitors(response):
#   visitors = 0 # in case there are no analytics available yet
#   for report in response.get('reports', []):
#     columnHeader = report.get('columnHeader', {})
#     metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

#     for row in report.get('data', {}).get('rows', []):
#       dateRangeValues = row.get('metrics', [])

#       for i, values in enumerate(dateRangeValues):
#         for metricHeader, value in zip(metricHeaders, values.get('values')):
#           visitors = value

#   return str(visitors)
def dataframe_to_list(df):
    # Create an empty list
    df_list = []

    # Iterate through the rows
    for _, row in df.iterrows():
        # Get the values for each column and append them to the list
        df_list.append([value for value in row])

    return df_list

@app.route('/chartpytrends', methods = ["GET", "POST"])
def chartpytrend():
    #pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})

    pytrends = TrendReq()
    kw_list = ['geneve']
    pytrends.build_payload(kw_list=kw_list, timeframe='today 5-y')
    trend_data = pytrends.interest_over_time()

    # Create a line chart using Matplotlib
    plt.plot(trend_data['geneve'])
    plt.xlabel('Date')
    plt.ylabel('Trend')

    # Save the chart to a PNG file
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the chart in base64
    chart_url = base64.b64encode(buf.getvalue()).decode()
    plt.clf()

    # Render the chart in an HTML template
    return render_template('plot.html', chart_url=chart_url)

        


