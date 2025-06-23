import pandas as pd
import os
import tempfile
from pathlib import Path

class File:
    def __init__(self, source, delimiter=','):
        self.delimiter = delimiter
        self.temp_path = None

        # Si la source est un fichier uploadé (UploadedFile)
        if hasattr(source, "read") and hasattr(source, "name"):
            self.uploaded_file = source
            self.filename = source.name
            self.is_uploaded_file = True
        else:
            # Si la source est un chemin (str ou Path)
            self.uploaded_file = None
            self.filename = Path(source).name
            self.temp_path = str(source)  # déjà prêt à être lu par pandas
            self.is_uploaded_file = False

    def save_temporarily(self):
        if self.is_uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", dir="./uploads/") as tmp:
                tmp.write(self.uploaded_file.read())
                self.temp_path = tmp.name

    def get_stats(self):
        if self.temp_path is None:
            self.save_temporarily()

        df = pd.read_csv(self.temp_path, delimiter=self.delimiter)

        stats = {
            "filename": self.filename,
            "shape": {
                "rows": df.shape[0],
                "columns": df.shape[1]
            },
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "describe": df.describe(include='all').to_dict(),
            "df": df
        }

        return stats
