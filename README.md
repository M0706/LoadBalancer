After cloning the repo

Step 1: Install FastAPI and Uvicorn
Make sure you have FastAPI and Uvicorn installed. You can install these packages using pip. Open your terminal and run the following command:

      pip install fastapi uvicorn


Step 2 Run the Backend Server (Run on three ports as given in the main file):

        uvicorn server:app --reload --port <port>

Step 3: Start the Load Balancer
In a new terminal, run the load balancer: 

      python main.py

Step 4: Test the Load Balancer Server using postman or curl. 

  curl --location 'http://127.0.0.1:8081/health' \
  --data ''
