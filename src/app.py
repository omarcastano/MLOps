from transformers import pipeline
from fastapi import FastAPI
import uvicorn
import nest_asyncio
from argparse import ArgumentParser

arg_parser = ArgumentParser()
arg_parser.add_argument("--model", default="cardiffnlp/twitter-roberta-base-sentiment-latest", help="model name")

# parse arguments
args = arg_parser.parse_args()

# import model from hugging face
model = pipeline(model=args.model)


## Deploying the model using fastAPI
app = FastAPI()


@app.get("/")
async def home():
    return "Congratulations! Your API is working as expected. Now head over to http://localhost:8000/docs"


@app.post("/predict/")
async def predict(data: dict):
    prediction = model.predict(data["text"])[0]
    return prediction


if __name__ == "__main__":
    # Allows the server to be run in this interactive environment
    nest_asyncio.apply()

    # define host
    host = "0.0.0.0"

    # sip up the server
    uvicorn.run(app, host=host, port=8000)
