
# Project Overview
GreenCart Simulation is a web application designed to simulate delivery operations for a logistics company. It helps managers run simulations based on available drivers, routes, and orders to analyze efficiency, profit, and delivery performance. The application includes:

React frontend for running simulations and viewing dashboards.
Flask backend: REST API managing drivers, routes, orders, and simulation logic.
Authentication for managers to securely access the system.

---

# Tech Stack

Frontend:
  - React.js
  - React Bootstrap
  - Axios (for HTTP requests)
  - Chart.js (for dashboard charts)
Backend:
  - Python 3.x
  - Flask (REST API)
  - SQLAlchemy (ORM)
Tools:
  - Git & GitHub (version control)
  - npm (frontend package manager)
  - pip (Python package manager)



# Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend folder:
    ```bash
    cd backend
    ```

2. Create a virtual environment :
    ```bash
    python -m venv venv
    venv\Scripts\activate       
    ```

3. Install backend dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the `backend/` folder with the required environment variables.

5. Run the backend server:

    ```bash
    python app.py
    ```



### Frontend Setup

1. Navigate to the frontend folder:
    ```bash
    cd frontend
    ```

2. Install frontend dependencies:
    ```bash
    npm install
    ```

3. Run the frontend development server:
    ```bash
    npm start
    ```

4. The app should open at `http://localhost:3000`


## Environment Variables

### Backend `.env` file 

```env
# Flask secret key for sessions
FLASK_SECRET_KEY=my_secret_key_here

```

## API Documentation

Interactive API docs are available at: [http://localhost:5000/docs](http://localhost:5000/docs)

You can explore all endpoints, see request parameters, response schemas, and try out the API directly from the browser.

