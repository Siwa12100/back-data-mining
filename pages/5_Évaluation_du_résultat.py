import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

st.set_page_config(page_title="Évaluation", layout="centered")
st.title("📊 Évaluation du modèle")

modele_type = st.session_state.get("modele_type", None)
modele = st.session_state.get("modele_objet", None)

if modele_type is None or modele is None:
    st.error("❌ Aucun modèle trouvé. Veuillez d'abord exécuter un entraînement.")
    st.stop()

if modele_type == "clustering":
    st.subheader("Résultats du Clustering")

    result_df = modele.get_result_dataframe()
    st.dataframe(result_df)

    st.markdown("### 📈 Visualisation PCA des clusters")
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(modele.scaled_X)
    reduced_df = pd.DataFrame(reduced, columns=["PC1", "PC2"])
    reduced_df["Cluster"] = modele.labels

    fig, ax = plt.subplots()
    sns.scatterplot(data=reduced_df, x="PC1", y="PC2", hue="Cluster", palette="tab10", ax=ax)
    ax.set_title("Projection PCA")
    st.pyplot(fig)

    try:
        stats = modele.get_cluster_stats()
        st.markdown("### 📊 Statistiques des clusters")
        st.dataframe(stats)
    except:
        st.info("Statistiques non disponibles.")

elif modele_type == "prediction":
    st.subheader("Résultats de la Prédiction")

    results = modele.evaluate()
    task_type = modele.task_type

    if task_type == "classification":
        st.metric("🎯 Accuracy", f"{results['accuracy']:.2%}")
        fig = modele.plot_confusion_matrix()
        if fig:
            st.pyplot(fig)

    elif task_type in ["régression", "regression"]:
        st.metric("📈 R²", f"{results['r2_score']:.2f}")
        st.metric("📉 MSE", f"{results['mse']:.2f}")

        st.markdown("### 📉 Courbe Réel vs Prédit")
        fig, ax = plt.subplots()
        ax.scatter(modele.y_test, modele.y_pred, alpha=0.6)
        ax.plot([modele.y_test.min(), modele.y_test.max()],
                [modele.y_test.min(), modele.y_test.max()],
                "r--", lw=2)
        ax.set_xlabel("y_test")
        ax.set_ylabel("y_pred")
        ax.set_title("Comparaison des valeurs réelles et prédites")
        st.pyplot(fig)

    st.markdown("### 📋 Prédictions")
    st.dataframe(modele.get_predictions_dataframe())

else:
    st.warning("Type de modèle non reconnu.")