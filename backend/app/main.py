from fastapi import FastAPI

app = FastAPI(
    title="DevPilot AI",
    version="1.0.0",
    description="An AI-powered developer workspace."
)


@app.get("/")
def root():
    return {
        "message": "Welcome to DevPilot AI 🚀"
    }