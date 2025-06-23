import streamlit as st
import pandas as pd

# Titre principal
st.set_page_config(page_title="Projet Data Mining", layout="centered")
st.title("📊 Projet Data Mining")
st.subheader("Partie I : Exploration initiale des données")

# Zone de chargement de fichier CSV
st.markdown("### 📁 Charger un fichier CSV")
uploaded_file = st.file_uploader("Glissez-déposez votre fichier ou cliquez pour en choisir un", type=["csv"])

# Si un fichier est chargé
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Fichier chargé avec succès !")
        
        # Aperçu des données
        st.markdown("### 👀 Aperçu des données")
        st.dataframe(df)

        # Infos basiques
        st.markdown("### ℹ️ Informations générales")
        st.write(f"**Nombre de lignes :** {df.shape[0]}")
        st.write(f"**Nombre de colonnes :** {df.shape[1]}")
        st.write("**Colonnes :**", list(df.columns))

        # Statistiques descriptives
        st.markdown("### 📈 Statistiques descriptives")
        st.write(df.describe(include='all'))

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {e}")
else:
    st.info("Veuillez charger un fichier CSV pour commencer.")
