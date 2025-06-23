import os
import pandas as pd


class File: 
    def __init__(self, filename, delimiter = ','):
        self.filename = filename
        self.file_path = os.path.join("./src/uploads/", filename)
        self.delimiter = delimiter

    def getStats(self):
        if not os.path.exists(self.file_path):
            return "Aucun fichier trouvé"

        df = pd.read_csv(self.file_path, delimiter=self.delimiter)

        stats = {
            "filename": self.filename,
            "shape": {
                "rows": df.shape[0],
                "columns": df.shape[1]
            },
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "describe": df.describe(include='all').to_dict()
        }

        return stats