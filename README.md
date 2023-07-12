# FedExTracker

# FedEx Tracking API Integration

This project demonstrates the integration of the FedEx Tracking API using a FastAPI backend and a Vue.js frontend. It allows users to enter a FedEx tracking number and retrieve the tracking information from the FedEx API.

## Features

- Accepts a FedEx tracking number and retrieves the tracking information.
- Uses FastAPI as the backend framework for handling API requests.
- Implements a Vue.js frontend to provide a user-friendly interface.
- Utilizes Docker and Docker Compose for easy deployment and containerization.

## Prerequisites

Before running the project, make sure you have the following prerequisites installed:

- Python 3.10 or higher
- Node.js
- Docker and Docker Compose

## Installation and Setup

1. Clone the repository:

   git clone git@github.com:YuraPotapov/FedExTracker.git

2. Set up the backend(only on local host, to debug for example):
   pip install -r requirements.txt

3. Set up the frontend(only on local host, to debug for example):
   cd frontend
   npm install

4. Create a .env file in the root directory and add the necessary environment variables:
   CLIENT_ID=<your_client_id>
   CLIENT_SECRET=<your_client_secret>

5. Build and run the Docker containers:
   docker compose up --build