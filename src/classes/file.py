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
        # Enregistre le fichier dans un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", dir="./src/uploads/") as tmp:
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
            "df": df  # Pour réutilisation directe dans Streamlit
        }

        return stats
