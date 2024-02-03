# Price Alert Application

## Overview

This is a price alert application that triggers an email when the user's target price for a cryptocurrency is achieved. The application utilizes Flask for the backend, JWT for user authentication, and various technologies for real-time price updates and email notifications.

## Features

- Create a REST API endpoint for users to create an alert (`/alerts/create/`).
- Create a REST API endpoint for users to delete an alert (`/alerts/delete/`).
- Create a REST API endpoint to fetch all alerts created by a user (`/alerts/`).
- Include status information in the response (created/deleted/triggered, etc.).
- Paginate the response for fetching alerts.
- Implement filtering options based on the status of alerts.
- Add user authentication using JWT tokens.
- Utilize Binance's WebSocket or Coingecko API for real-time price updates.
- Send email notifications to users when the target price is reached.
- Add a caching layer for the "fetch all alerts" endpoint using Redis.
- Store data in a PostgreSQL database.
- Use Rabbit MQ / Redis as a message broker for sending emails.
- Bundle the application inside a Docker container.

## Technologies Used

- Flask (Python)
- JWT for user authentication
- PostgreSQL for data storage
- Binance WebSocket or Coingecko API for real-time price updates
- Redis for caching
- Rabbit MQ for message brokering
- Docker for containerization

## Getting Started

### Prerequisites

- Python (version 3.7 or later)
- Docker
- PostgreSQL
- Rabbit MQ

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RAHULSAINI830/Price-Alert-Application.git

to optimize the fetching of alerts and relies on Rabbit MQ for asynchronous email notifications.


Install dependencies:

pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root and add the necessary environment variables.

Build and run the Docker container:

docker-compose up -d
Visit http://localhost:5000 to access the application.


# I am attaching API Output:-


login


![Login](https://github.com/RAHULSAINI830/Price-Alert-Application/assets/96569692/cf801978-cbb3-4170-8858-22dc95bc0d0e)

Creating Alert

![Create](https://github.com/RAHULSAINI830/Price-Alert-Application/assets/96569692/c437bfea-3fdc-4222-ab0f-7b17f4cdffa6)

Deleting Alert

![Delete](https://github.com/RAHULSAINI830/Price-Alert-Application/assets/96569692/dfd26259-ed8e-4fea-93c6-a4177ed0611c)



Usage
Use the provided API endpoints to create, delete, and fetch alerts.
Authenticate users using the login endpoint (/login).
Real-time price updates will be fetched using Binance WebSocket or Coingecko API.
Emails will be sent to users when their target price is reached.
Acknowledgments
This project was developed as part of an assignment for tanX.fi. Special thanks to the team for the opportunity.

Author


Rahul Saini


8306885992
