from flask import Flask, request, jsonify
import requests
app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(source_currency)
    print(amount)
    print(target_currency)

    final_amount = fetch_conversion_factor(source_currency, target_currency, amount)
    final_amount = round(final_amount, 2)
    print(final_amount)

    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }
    return jsonify(response)


def fetch_conversion_factor(source, target, amount):
    url = "https://api.apilayer.com/currency_data/convert?to={}&from={}&apikey=<your-api-key-goes-here>&amount={}".format(target, source, amount)
    response = requests.get(url)
    response = response.json()
    return response['result']


if __name__ == "__main__":
    app.run(debug=True)
