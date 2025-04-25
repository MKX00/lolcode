from flask import Flask, render_template, request, jsonify
import stripe
import os
import json

app = Flask(__name__)
stripe.api_key = os.getenv('STRIPE_KEY')

def check_stripe_connection():
    try:
        stripe.Customer.list(limit=1)
        return True, "Connected successfully"
    except stripe.error.AuthenticationError:
        return False, "Invalid API key"
    except Exception as e:
        return False, str(e)

def check_webhook_config():
    try:
        webhooks = stripe.WebhookEndpoint.list()
        if not webhooks.data:
            return False, "No webhooks configured"
        return True, f"Found {len(webhooks.data)} webhook(s)"
    except Exception as e:
        return False, str(e)

def check_payment_methods():
    try:
        methods = stripe.PaymentMethod.list(type="card", limit=1)
        return True, "Payment methods available"
    except Exception as e:
        return False, str(e)

def check_products():
    try:
        products = stripe.Product.list(limit=1)
        if not products.data:
            return False, "No products found"
        return True, f"Found {len(products.data)} product(s)"
    except Exception as e:
        return False, str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/debug-stripe', methods=['POST'])
def debug_stripe():
    results = {
        "connection": check_stripe_connection(),
        "webhooks": check_webhook_config(),
        "payment_methods": check_payment_methods(),
        "products": check_products(),
        "mode": "test" if "test" in stripe.api_key else "live",
        "api_version": stripe.api_version
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)