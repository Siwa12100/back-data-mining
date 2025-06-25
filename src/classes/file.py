import pandas as pd
import tempfile
from pathlib import Path

class File:
    def __init__(self, source, delimiter=','):
        self.delimiter = delimiter
        self.temp_path = None

        if hasattr(source, "read") and hasattr(source, "name"):
            self.uploaded_file = source
            self.filename = source.name
            self.is_uploaded_file = True
        else:
            self.uploaded_file = None
            self.filename = Path(source).name
            self.temp_path = str(source)
            self.is_uploaded_file = False

    def save_temporarily(self):
        if self.is_uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", dir="./uploads/") as tmp:
                tmp.write(self.uploaded_file.read())
                self.temp_path = tmp.name

    def get_stats(self):
        # Choix de la source du fichier
        if self.is_uploaded_file:
            self.save_temporarily()

        # Lecture à partir de temp_path
        df = pd.read_csv(self.temp_path, delimiter=self.delimiter)

        # Tentative de conversion des colonnes object → numeric si possible
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        stats = {
            "filename": self.filename,
            "shape": {"rows": df.shape[0], "columns": df.shape[1]},
            "columns": list(df.columns),
            "dtypes": dict(df.dtypes.astype(str)),
            "missing_values": dict(df.isnull().sum()),
            "df": df
        }
        return stats
