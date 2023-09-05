import fastapi
import uvicorn
import nest_asyncio
from pydantic import create_model
import pandas as pd
from src.model import MyModel
from src.etl import MyETL
from argparse import ArgumentParser

arg_parser = ArgumentParser()

# model arguments
arg_parser.add_argument("--dataset", type=str, default="titanic", help="Dataset to train the model")
arg_parser.add_argument("--num_input_features", nargs="+", type=str, default=["age"], help="Numerical input features")
arg_parser.add_argument("--cat_input_features", nargs="+", type=str, default=["class"], help="Categorical input features")
arg_parser.add_argument("--target_var", type=str, default="survived", help="Target variable to train the model")

# parse arguments
args = arg_parser.parse_args()

## Replace with your actual database connection details
db_host = "maria_db"
# instance the etl
etl = MyETL(table_name=args.dataset, db_host=db_host)


## load dataset
X_train, X_test, y_train, y_test = etl.get_data(
    num_var=args.num_input_features,
    cat_var=args.cat_input_features,
    target_var=args.target_var,
)


## define model
model = MyModel(num_var=args.num_input_features, cat_var=args.cat_input_features)

## fit the model
model.fit(X_train, y_train)

## declare app
app = fastapi.FastAPI()


# define pydantic model
def generate_model_from_dict(data_dict):
    fields = {}
    for key, value in data_dict.items():
        fields[key] = (type(value), value)
    return create_model("Item", **fields)


# define a pydantic model
my_dict = X_train.sample(1).to_dict(orient="records")[0]
Item = generate_model_from_dict(my_dict)


# home page
@app.get("/")
def index():
    return {"message": "Your app is running ! :)"}


# model inference
@app.post("/predict/")
def predict(data: Item) -> dict:
    data = data.model_dump()
    data = pd.DataFrame(data, index=[0])

    label = model.predict(data)
    prob = model.predict_proba(data)

    result = {"label": str(label[0]), "probability": str(round(prob[0][label][0], 3))}

    return result


if __name__ == "__main__":
    nest_asyncio.apply()
    host = "0.0.0.0"

    # launch the app using uvicorn
    uvicorn.run(app, host=host, port=8000)
