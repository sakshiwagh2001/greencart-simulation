
# Project Overview & Purpose
GreenCart Simulation is a comprehensive logistics and delivery management application designed to help businesses optimize their delivery operations. It provides tools to manage drivers, routes, and orders effectively, and to simulate real-world delivery scenarios to maximize profitability and efficiency.

Key Features:
 - Driver Management: Track available drivers, their working hours, and assign delivery routes efficiently.

 - Route Management: Define and manage routes with varying distances and traffic conditions.

 - Order Management: Maintain details of delivery orders including value, delivery time, and associated routes.

 - Simulation Engine: Run simulations to analyze how different factors—like the number of drivers, start times, and maximum working hours—impact overall delivery performance and profitability.

 - Performance Metrics: Visual dashboards present key insights such as on-time delivery rates, fuel costs, and efficiency scores to support data-driven decision-making.

Purpose:
- The core purpose of GreenCart Simulation is to empower delivery businesses by providing a realistic, data-driven simulation environment that helps:

- Identify bottlenecks and inefficiencies in delivery processes.

- Assess the impact of driver availability and working hours on delivery punctuality.

- Evaluate financial outcomes including total profit after accounting for penalties and fuel costs.

- Make informed decisions on resource allocation, route planning, and scheduling to improve customer satisfaction and reduce operational costs.

This application is ideal for logistics managers, delivery companies, and startups aiming to scale their delivery network while maintaining high performance and cost-effectiveness.


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

