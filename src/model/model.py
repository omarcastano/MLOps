# import libraries
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


class MyModel:
    def __init__(self, num_var, cat_var) -> None:
        if num_var[0] == "None":
            num_var = []
        if cat_var[0] == "None":
            cat_var = []

        # define numerical preprocessing steps
        num_preprocess = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        # define categorical preprocessing steps
        cat_preprocess = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="most_frequent", fill_value="missing")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )
        # define ColumneTransformer
        preprocessor = ColumnTransformer(
            [
                ("num", num_preprocess, num_var),
                ("cat", cat_preprocess, cat_var),
            ]
        )
        # define model

        self.model = Pipeline(
            [
                ("preprocessor", preprocessor),
                ("classifier", LogisticRegression()),
            ]
        )

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def predict_proba(self, X_test):
        return self.model.predict_proba(X_test)

    def score(self, X_test, y_test):
        return self.model.score(X_test, y_test)

    def get_sklearn_model(self):
        return self.model
