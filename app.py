import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import httplib2
import json
from wtform_fields import *


app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
# set secret key to cross site requset forgery
# to generate a token when WTF submitted
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

# Main route display the form with get requset
# redirect to convert route with post request
@app.route('/', methods=['GET', 'POST'])
def index():
    # get Currency Convert Form from WTF
    conv_form = CurrencyCovert()
    # convert if the validation success
    if conv_form.validate_on_submit():
        # Get the data from the form field
        src_currency = conv_form.src_currency.data
        dest_currency = conv_form.dest_currency.data
        amount = conv_form.amount.data
        date = conv_form.date.data
        # redirect to convert route
        # Pass the form's data as a parameter to convert route
        return redirect(url_for('convert',
                                src_currency=src_currency,
                                dest_currency=dest_currency,
                                amount=amount,
                                date=date))

    return render_template('index.html', form=conv_form)


# Get the data from the URL
# Accept only get request
@app.route('/convert', methods=['GET'])
def convert():
    src = request.args.get('src_currency').upper()
    dest = request.args.get('dest_currency').upper()
    amount = float(request.args.get('amount'))
    date = request.args.get('date')

    # Declare the data dict
    data = {}
    if src == dest:
        data['amount'] = amount
        data['currency'] = dest
        return jsonify(data)

    # Make sure the date in the format YYYY-MM-DD
    # else return empty JSON
    try:
        time = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify(data)
    else:
        url = "https://api.exchangeratesapi.io/{}?base={}&symbols={}".format(date, src, dest)

    # use HTTP client library, to be able to send GET request
    h = httplib2.Http()
    # convert the JSON format to python dictionary
    result = json.loads(h.request(url, 'GET')[1])
    # parse the result and get the rate value
    if 'rates' in result:
        rate = result['rates'][dest]
        data['amount'] = amount * rate
        data['currency'] = dest

    return jsonify(data)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
