from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import streamlit as st
import pandas as pd
import seaborn as sns

from src.classes.prediction import Prediction
from src.classes.clustering import Clustering

st.set_page_config(page_title="Pré-traitement", layout="centered")
st.title("Partie IV : Clustering ou prédiction")

df = st.session_state.get("df", None)
delimiter = st.session_state.get("delimiter", ",")

if df is not None:
    st.write("✅ Données récupérées depuis la session")
    st.dataframe(df.head())
else:
    st.warning("⚠️ Aucune donnée trouvée. Retournez à l'étape d'upload.")
    st.stop()

mode = st.radio("Souhaitez-vous effectuer :", options=["Clustering", "Prédiction"])

if mode == "Clustering":
    num_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    if not num_cols:
        st.error("❌ Aucune colonne numérique disponible pour le clustering.")
        st.stop()

    st.markdown("### 🧪 Choix des variables pour le clustering")
    selected_cols = st.multiselect("Sélectionnez les colonnes à utiliser", options=num_cols, default=num_cols)

    if selected_cols:
        clustering = Clustering(df)
        clustering.set_features(selected_cols)

        st.markdown("### ⚙️ Choix de l'algorithme de clustering")

        algo = st.selectbox(
            "Algorithme",
            options=["K-Means", "DBSCAN", "HCA (Hierarchical Clustering)"]
        )

        if algo == "K-Means":
            n_clusters = st.slider("Nombre de clusters (K)", min_value=2, max_value=10, value=3)
        elif algo == "DBSCAN":
            eps = st.slider("ε (rayon de voisinage)", min_value=0.1, max_value=10.0, value=0.5, step=0.1)
            min_samples = st.slider("Min. samples", min_value=1, max_value=10, value=5)
        elif algo == "HCA (Hierarchical Clustering)":
            n_clusters = st.slider("Nombre de clusters", min_value=2, max_value=10, value=3)

        if st.button("🚀 Lancer le clustering"):
            try:
                if algo == "K-Means":
                    clustering.run_kmeans(n_clusters=n_clusters)
                elif algo == "DBSCAN":
                    clustering.run_dbscan(eps=eps, min_samples=min_samples)
                elif algo == "HCA (Hierarchical Clustering)":
                    clustering.run_hca(n_clusters=n_clusters)

                st.session_state["modele_type"] = "clustering"
                st.session_state["modele_objet"] = clustering
                st.success("✅ Clustering terminé. Redirection vers l’évaluation...")
                st.switch_page("pages/5_Évaluation_du_résultat.py")

            except Exception as e:
                st.error(f"❌ Erreur lors du clustering : {e}")
    else:
        st.info("Veuillez sélectionner au moins une colonne pour démarrer.")
elif mode == "Prédiction":
    target_col = st.selectbox("📌 Sélectionnez la variable cible", options=df.columns)
    feature_cols = st.multiselect("🧪 Sélectionnez les variables explicatives", options=[col for col in df.columns if col != target_col])

    if feature_cols and target_col: 
        task_type = st.radio("Type de problème :", options=["Classification", "Régression"])
        
        algo = None
        model_params = {}

        if task_type == "Classification":
            algo = st.selectbox("Choix de l'algorithme", ["Random Forest", "Logistic Regression"])
            if algo == "Random Forest":
                model_params["n_estimators"] = st.slider("Nombre d'arbres", 10, 300, 100)

        elif task_type == "Régression":
            algo = st.selectbox("Choix de l'algorithme", ["Régression Linéaire", "Arbre de régression"])
            if algo == "Arbre de régression":
                model_params["max_depth"] = st.slider("Profondeur max", 1, 20, 5)

        if st.button("🚀 Entraîner le modèle"):
            try:
                predictor = Prediction(df, features=feature_cols, target=target_col, task_type=task_type)
                predictor.split()
                predictor.set_model(algo, **model_params)
                predictor.train()

                st.session_state["modele_type"] = "prediction"
                st.session_state["modele_objet"] = predictor
                st.success("✅ Modèle entraîné. Redirection vers l’évaluation...")
                st.switch_page("pages/5_Évaluation_du_résultat.py")

            except Exception as e:
                st.error(f"❌ Erreur : {e}")
        else:
            st.info("Veuillez sélectionner les colonnes d'entrée et la cible.")