# Safe Route Calculation API

This API calculates the safest route between a start and an end location, using flood risk data from the UP NOAH dataset, which is pre-loaded via a remote database.

---

## Requirements

1. **Python**: Ensure Python 3.13 is installed.
   - To verify, run:
     ```bash
     python3.13 --version
     ```
   - If not installed, download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Database Credentials**: Add a `.env` file in the main directory containing the database credentials. This file should be formatted as follows:
   ```python
      DB_CACHE_NAME = ""
      DB_CACHE_USER = ""
      DB_CACHE_PASSWORD = ""
      DB_CACHE_HOST = ""
      DB_CACHE_PORT = ""
      DB_CACHE_TABLE_NAME = ""
      DB_CACHE_URL = ""
   ```

---

## Github Installation 
### Mac Installation

1. Clone the repository or download the source code.

2. Navigate to the project directory.

3. Set up a virtual environment:
   ```bash
   python3.13 -m venv .venv
   ```

4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Windows Installation

1. Clone the repository or download the source code.

2. Navigate to the project directory.

3. Set up a virtual environment:
   ```bash
   python3.13 -m venv .venv
   ```

4. Activate the virtual environment:
   ```bash
   cd .venv/bin
   activate
   ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Docker Installation

1. Install Docker
2. Pull the image from [Docker Hub](https://hub.docker.com/r/epilefs/buhay-api)
   ```bash
   docker pull epilefs/buhay-api
   ```
3. Run the downloaded image
   ```bash
   docker run -p 8080:8080 epilefs/buhay-api
   ```
4. By default, the API will be available at:
   ```
   http://0.0.0.0:8080
   ```

---

## Running the FastAPI Server

1. Start the development server:
   ```bash
   fastapi dev main.py
   ```

2. By default, the API will be available at:
   ```
   http://127.0.0.1:8000
   ```
   
---

## Using the `directions` endpoint

1. Install Postman.
2. Use the `/directions` endpoint to calculate the safest route.
   - If running with the fastapi server, use `http://127.0.0.1:8000/directions`
   - If running with Docker, use `http://0.0.0.0:8080/directions`

   In the request body, the endpoint requires a JSON parameter of the form
   ```
   {
      "start" : "<longitude>,<latitude>",
      "end" : "<longitude>,<latitude>" 
   }
   ```

3. The response will be in the form
   ```
   {
      "route" : {
            "duration": float,
            "distanceKm": float
      },

      "geojson" : <geojson_data>,
      "message" : str
   }
   ```

---

## Using the `tsp` endpoint

The _tsp endpoint_ accepts a POST Request at the `/tsp` path. This request contains a list of <b>n</b> `Point`s which follows the format below.
1. Install Postman.
2. Use the `/tsp` endpoint to calculate the safest route.
   - If running with the fastapi server, use `http://127.0.0.1:8000/tsp`
   - If running with Docker, use `http://0.0.0.0:8080/tsp`
  
   In the request body, the endpoint requires a JSON parameter of the form
   ```
   [
      {
         "start": {
           "coordinates": [
             longitude,
             latitude
           ]
         },
         "other_points": [
           {
             "coordinates": [
               longitude,
               latitude
             ],
             ...
           }
         ]
      }
   ]
   ```
3. The response will be in the form
   ```
   [
      {
         "start" : [<longitude>,<latitude>],
         "end" : [<longitude>,<latitude>],
         "data" : <geojson_data>
      },
      ...
   ]
   ```

---

## Running Tests with Pytest

1. Ensure the virtual environment is activated:
   ```bash
   source .venv/bin/activate
   ```

2. Run the test suite using `pytest`:
   ```bash
   pytest
   ```

3. View the test results in the terminal. Pytest will display detailed feedback about the tests.

---

## Notes

- The UP NOAH dataset is pre-loaded and does not require manual setup.
- Modify the `host` and `port` in the `fastapi` command if needed to match your environment.
- Ensure the `.env` file is correctly configured for database access.
- Route requests with a location outside Quezon City could result to an incorrect route data since flood data is limited to Quezon City only.

---

For further assistance, refer to the FastAPI [documentation](https://fastapi.tiangolo.com/) or contact the project maintainer.
