from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

class Clustering:
    def __init__(self, dataframe):
        self.df = dataframe
        self.X = None
        self.labels = None

    def set_features(self, columns):
        self.X = self.df[columns].dropna()
        self.scaled_X = StandardScaler().fit_transform(self.X)

    def run_kmeans(self, n_clusters=3):
        model = KMeans(n_clusters=n_clusters)
        self.labels = model.fit_predict(self.scaled_X)
        return self.labels

    def run_dbscan(self, eps=0.5, min_samples=5):
        model = DBSCAN(eps=eps, min_samples=min_samples)
        self.labels = model.fit_predict(self.scaled_X)
        return self.labels

    def run_hca(self, n_clusters=3):
        model = AgglomerativeClustering(n_clusters=n_clusters)
        self.labels = model.fit_predict(self.scaled_X)
        return self.labels

    def get_result_dataframe(self):
        if self.labels is not None:
            result_df = self.X.copy()
            result_df["Cluster"] = self.labels
            return result_df
        return None
    
    def get_cluster_stats(self):
        if self.labels is None:
            raise RuntimeError("Aucun clustering effectué.")

        df_stats = self.X.copy()
        df_stats["Cluster"] = self.labels
        stats = df_stats.groupby("Cluster").agg(["mean", "count"])
        return stats

    def get_centroids(self):
        from sklearn.cluster import KMeans
        if not isinstance(self.model, KMeans):
            raise RuntimeError("Les centroïdes ne sont disponibles que pour KMeans.")
        return self.model.cluster_centers_