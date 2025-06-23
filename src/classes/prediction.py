from matplotlib import pyplot as plt
import pandas as pd
import seaborn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, r2_score, mean_squared_error

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor


class Prediction:
    def __init__(self, df: pd.DataFrame, features: list, target: str, task_type: str):
        self.df = df.dropna(subset=features + [target])
        self.X = pd.get_dummies(self.df[features])
        self.y = self.df[target]
        self.task_type = task_type.lower()
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None

    def split(self, test_size=0.2, random_state=42):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state
        )

    def set_model(self, name: str, **params):
        if self.task_type == "classification":
            if name == "Random Forest":
                self.model = RandomForestClassifier(**params)
            elif name == "Logistic Regression":
                self.model = LogisticRegression(max_iter=1000, **params)
            else:
                raise ValueError("Modèle de classification non reconnu.")
        elif self.task_type in ["régression", "regression"]:
            if name == "Régression Linéaire":
                self.model = LinearRegression(**params)
            elif name == "Arbre de régression":
                self.model = DecisionTreeRegressor(**params)
            else:
                raise ValueError("Modèle de régression non reconnu.")
        else:
            raise ValueError("Type de tâche non reconnu : classification ou régression")

    def train(self):
        if self.model is None:
            raise RuntimeError("Aucun modèle défini.")
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def evaluate(self):
        if self.y_pred is None:
            raise RuntimeError("Le modèle n'a pas encore été entraîné.")
        if self.task_type == "classification":
            return {
                "accuracy": accuracy_score(self.y_test, self.y_pred)
            }
        elif self.task_type in ["régression", "regression"]:
            return {
                "r2_score": r2_score(self.y_test, self.y_pred),
                "mse": mean_squared_error(self.y_test, self.y_pred)
            }

    def get_predictions_dataframe(self):
        return pd.DataFrame({
            "y_test": self.y_test,
            "y_pred": self.y_pred
        }).reset_index(drop=True)

    def plot_confusion_matrix(self):
        if self.task_type != "classification":
            return None
        cm = confusion_matrix(self.y_test, self.y_pred)
        fig, ax = plt.subplots()
        seaborn.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Prédit")
        ax.set_ylabel("Réel")
        ax.set_title("Matrice de confusion")
        return fig