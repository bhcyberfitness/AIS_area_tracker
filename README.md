# Vessel Dashboard

This project was created 23-24 July 2024 to help me learn Python and JavaScript. The provides a dashboard to visualize nearby vessels to a specified position. It includes a backend service to handle vessel data and a frontend to display the information.

## Features

- Display nearby vessels within a specified distance.
- Update threat levels of vessels.
- Real-time data streaming from AIS service.

## Getting Started

### Prerequisites

- Python 3.7+
- Node.js
- FastAPI
- Uvicorn
- WebSockets
- Haversine

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/vessel-dashboard.git
    cd vessel-dashboard
    ```

2. **Set up the backend:**
    - Navigate to the backend directory:
        ```bash
        cd backend
        ```
    - Create and activate a virtual environment:
        ```bash
        python3 -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`
        ```
    - Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```
    - Set the AIS API key in your environment:
        ```bash
        export AIS_API_KEY=your_api_key  # On Windows use `set AIS_API_KEY=your_api_key`
        ```
    - Run the FastAPI server:
        ```bash
        uvicorn main:app --reload
        ```

3. **Set up the frontend:**
    - Navigate to the frontend directory:
        ```bash
        cd ../frontend
        ```
    - Install the required packages:
        ```bash
        npm install
        ```
    - Start the development server:
        ```bash
        npm start
        ```

### Usage

- Access the frontend dashboard at `http://localhost:3000`.
- The backend API is available at `http://127.0.0.1:8000`.

### API Endpoints

- **Get all vessels:**
    ```
    GET /vessels
    ```
- **Get vessels within a distance:**
    ```
    GET /vessels_within_distance?threshold={distance}
    ```
- **Update vessel threat level:**
    ```
    PUT /vessels/{mmsi}
    Body: { "threat": "new_threat_level" }
    ```
