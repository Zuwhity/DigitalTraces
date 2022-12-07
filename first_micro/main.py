from flask import Flask, render_template, request, url_for
from markupsafe import escape # to escape user inputs and so avoid injection attacks
import requests

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
