# AIS Area Tracker

This project was created 23-24 July 2024 to help me learn Python and JavaScript. The provides a dashboard to visualize nearby vessels to a specified position. It includes a backend service to handle vessel data and a frontend to display the information.

## Features

- Display all vessels within a specified bounding box, using AIS messages from aisstream.io.
- Set threat levels of vessels to blue (friendly), white (neutral) or red (hostile).
- Display all vessels within a specified range of the point, or those that will enter the range in the future based on current course and speed. (There is no frontend for this feature yet but it is accessed at GET /vessels_within_distance?threshold={distance})

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
    git clone https://github.com/bhcyberfitness/AIS_area_tracker.git
    cd AIS_area_tracker
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
    - Create the file apikey in backend with aisstream.io API key (these are free):
       
    - Run the FastAPI server:
        ```bash
        python main.py
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
## Future Capabilties

This project was a good exercise in testing my capabilities in Python and JavaScript and hacking together a solution quickly, and I may not revisit this in the future. If I do, there are a number of improvements to be made, such as the following:

### Threshold Distance Frontend

Currently there is an API endpoint for getting all vessels within a certain distance of the point plus those who will be at any point in the next hour. This is computed by dead reckoning the current position, course and speed. It would be useful to visualise this data, and this would be easy as the API endpoint returns this data in the exact same format as the total vessel list.

### Dead Reckon old data

The backend will stop receiving data from vessels that leave the bounding box, or from those that for some reason stop transmitting AIS messages. Currently the tool does not record timestamps for messages so it won't differentiate between new or old messages, instead relying on all vessels being up to date all the time. By dead reckoning old data the tool will be able to predict future positions when it stops receiving data.

### Prune irrelevant data

The tool currently will never delete vessels from the list. If one travels outside the area of interest, it will hold the last state indefinitely. This wastes memory but more importantly it incorrectly represents what vessels are nearby.

### Pre-configured vessel threat lists

Currently the tool automatically initialises all vessels to a white (neutral) threat level, relying on user input to change threat levels of vessels. It would be useful to automatically assign different threat levels based on pre-defined conditions, such as MMSI.

### Interactive map

No situational awareness tool is truly as effective as it could be as just a list of latitude/longitudes. Displaying all vessels as well as the pre-defined point, radius and AIS message bounding box on a map would be more effective for displaying data to the user.