from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
import requests
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import redis
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_name:your_password@localhost/price_alerts'
db = SQLAlchemy(app)


# In-memory storage for alerts
alerts = []
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Binance WebSocket or Coingecko API for real-time price updates
# Implement the logic to connect to Binance WebSocket or use the Coingecko API

# Function to send email
def send_email(user_email, alert_status, coin_name, target_price):
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_email_password'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = user_email
    message['Subject'] = f'Crypto Alert - {alert_status} - {coin_name}'

    body = f'The alert for {coin_name} has been {alert_status} at the target price of {target_price}.'
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, message.as_string())

# Function to check alerts and trigger actions
def check_alerts():
    while True:
        for alert in alerts:
            # Implement logic to get real-time price updates for the alert's cryptocurrency
            current_price = get_current_price(alert['coin_symbol'])

            if current_price is not None:
                if alert['target_price'] >= current_price:
                    # Alert triggered
                    alert['status'] = 'triggered'
                    print("triggered")
                    send_email(alert['user_email'], 'triggered', alert['coin_name'], alert['target_price'])

        # Sleep for some time before checking alerts again
        threading.Event().wait(60)  # sleep for 60 seconds

# Get current price of a cryptocurrency from Coingecko API
def get_current_price(coin_symbol):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_symbol}&vs_currencies=usd'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get(coin_symbol, {}).get('usd')
    else:
        return None

# Endpoint to create an alert
@app.route('/alerts/create/', methods=['POST'])
@jwt_required()
def create_alert():
    data = request.get_json()

    coin_symbol = data.get('coin_symbol')
    coin_name = data.get('coin_name')
    target_price = data.get('target_price')
    user_email = data.get('user_email')

    alert = {
        'coin_symbol': coin_symbol,
        'coin_name': coin_name,
        'target_price': target_price,
        'user_email': user_email,
        'status': 'created'
    }

    alerts.append(alert)
    redis_client.set('alerts', str(alerts))  # Store alerts in Redis for caching
    current_price = get_current_price(coin_symbol)
    if current_price is not None and target_price >= current_price:
        alert['status'] = 'triggered'
        send_email(user_email, 'triggered', coin_name, target_price)


    return {'message': 'Alert created successfully'}, 201

# Endpoint to delete an alert
@app.route('/alerts/delete/', methods=['DELETE'])
@jwt_required()
def delete_alert():
    data = request.get_json()
    coin_symbol = data.get('coin_symbol')
    user_email = data.get('user_email')

    for alert in alerts:
        if alert['coin_symbol'] == coin_symbol and alert['user_email'] == user_email:
            alerts.remove(alert)
            redis_client.set('alerts', str(alerts))  # Update alerts in Redis for caching
            send_email(user_email, 'deleted', alert['coin_name'], alert['target_price'])
            return {'message': 'Alert deleted successfully'}

    return {'message': 'Alert deleted successfully'}, 404

# Endpoint to fetch all alerts with pagination and filtering
@app.route('/alerts/', methods=['GET'])
@jwt_required()
def get_alerts():
    status_filter = request.args.get('status')

    if redis_client.exists('alerts'):
        alerts_data = eval(redis_client.get('alerts').decode('utf-8'))
    else:
        alerts_data = alerts

    if status_filter:
        filtered_alerts = [alert for alert in alerts_data if alert['status'] == status_filter]
    else:
        filtered_alerts = alerts_data

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    paginated_alerts = filtered_alerts[start_index:end_index]

    return jsonify({'alerts': paginated_alerts, 'total_alerts': len(filtered_alerts)})

# Endpoint for user login (to generate JWT token)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Here, you can perform actual user authentication
    # For simplicity, assuming user is valid, generate JWT token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

if __name__ == '__main__':
    # Start the background thread for checking alerts
    alert_thread = threading.Thread(target=check_alerts)
    alert_thread.start()

    app.run(debug=True)

