import pandas as pd
import os
import tempfile


class File:
    def __init__(self, uploaded_file, delimiter=','):
        self.uploaded_file = uploaded_file
        self.delimiter = delimiter
        self.filename = uploaded_file.name
        self.temp_path = None

    def preview(self):
        df = pd.read_csv(self.file_path, delimiter=self.delimiter)
        return df.head(3), df.tail(3)

    def save_temporarily(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", dir="./uploads/") as tmp:
            tmp.write(self.uploaded_file.read())
            self.temp_path = tmp.name

    def get_stats(self):
        df = pd.read_csv(self.uploaded_file, delimiter=self.delimiter)

        for col in df.columns:
            if df[col].dtype == object:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        stats = {
            "filename": getattr(self.uploaded_file, "name", "Fichier CSV"),
            "shape": {"rows": df.shape[0], "columns": df.shape[1]},
            "columns": list(df.columns),
            "dtypes": dict(df.dtypes.astype(str)),
            "missing_values": dict(df.isnull().sum()),
            "df": df
        }
        return stats
