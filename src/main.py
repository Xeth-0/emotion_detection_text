from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_text_emotion

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict")
async def predict_emotion(text: str):
    response = predict_text_emotion(text)
    return {
        "probabilities": response["probabilities"],
        "top_emotion": response["top_emotion"],
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10000)

