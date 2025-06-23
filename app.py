import streamlit as st
from src.classes.file import File

st.set_page_config(page_title="Projet Data Mining", layout="centered")
st.title("📊 Projet Data Mining")
st.subheader("Partie I : Exploration initiale des données")

st.markdown("### 📁 Charger un fichier CSV")
uploaded_file = st.file_uploader("Glissez-déposez votre fichier ou cliquez pour en choisir un", type=["csv"])

if uploaded_file is not None:
    try:
        fichier = File(uploaded_file)
        stats = fichier.get_stats()
        df = stats["df"]

        st.success("✅ Fichier chargé avec succès !")
        st.markdown("### 👀 Aperçu des données")
        st.dataframe(df)

        st.markdown("### ℹ️ Informations générales")
        st.write(f"**Nom du fichier :** {stats['filename']}")
        st.write(f"**Nombre de lignes :** {stats['shape']['rows']}")
        st.write(f"**Nombre de colonnes :** {stats['shape']['columns']}")
        st.write("**Colonnes :**", stats["columns"])
        st.write("**Types de données :**", stats["dtypes"])
        st.write("**Valeurs manquantes :**", stats["missing_values"])

        st.markdown("### 📈 Statistiques descriptives")
        st.write(stats["describe"])

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement du fichier : {e}")
else:
    st.info("Veuillez charger un fichier CSV pour commencer.")
