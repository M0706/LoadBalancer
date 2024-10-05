from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()

# Define a Pydantic model to structure the JSON response
class HealthResponse(BaseModel):
    status: str
    message: str

# Create the /health endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", message="The server is running smoothly!")

# To run the app: uvicorn main:app --reload
