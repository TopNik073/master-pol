from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return "Test app"


if __name__ == "__main__":
    uvicorn.run(app)
