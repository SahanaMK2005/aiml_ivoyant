from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from agents.orchestrator_agent import OrchestratorAgent


app = FastAPI()

# Serve static files (CSS and JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Serve HTML page
@app.get("/")
def home():
    return FileResponse("templates/index.html")


# API endpoint
@app.get("/study")
def study(topic: str):

    orchestrator = OrchestratorAgent()

    result = orchestrator.process_topic(topic)

    return result