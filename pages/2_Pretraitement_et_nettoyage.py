import streamlit as st
import pandas as pd
from src.classes.file import File

st.set_page_config(page_title="Pré-traitement", layout="centered")
st.title("🧹 Partie II : Pré-traitement et nettoyage des données")

# ✅ Vérifie qu'on a bien tout en session
if "csv_file" not in st.session_state or "delimiter" not in st.session_state:
    st.warning("Veuillez d'abord charger un fichier dans l'étape 1.")
    st.stop()

uploaded_file = st.session_state["csv_file"]
delimiter = st.session_state["delimiter"]

fichier = File(uploaded_file, delimiter=delimiter)
df = fichier.get_stats()["df"]

st.markdown("### 🧪 Sélection des colonnes à traiter")
colonnes_numeriques = df.select_dtypes(include='number').columns.tolist()
colonnes_choisies = st.multiselect("Colonnes numériques à traiter :", colonnes_numeriques)

if colonnes_choisies:
    st.markdown("### 🧱 Gestion des valeurs manquantes")
    methode_na = st.selectbox("Méthode de traitement :", ["Supprimer les lignes", "Remplir par la moyenne", "Remplir par la médiane"])

    if methode_na == "Supprimer les lignes":
        df = df.dropna(subset=colonnes_choisies)
    elif methode_na == "Remplir par la moyenne":
        for col in colonnes_choisies:
            df[col] = df[col].fillna(df[col].mean())
    elif methode_na == "Remplir par la médiane":
        for col in colonnes_choisies:
            df[col] = df[col].fillna(df[col].median())

    st.markdown("### ⚖️ Normalisation des colonnes")
    normalisation = st.selectbox("Méthode de normalisation", ["Aucune", "Min-Max", "Z-score"])

    if normalisation == "Min-Max":
        for col in colonnes_choisies:
            min_val, max_val = df[col].min(), df[col].max()
            df[col] = (df[col] - min_val) / (max_val - min_val)
    elif normalisation == "Z-score":
        for col in colonnes_choisies:
            mean, std = df[col].mean(), df[col].std()
            df[col] = (df[col] - mean) / std

    st.markdown("### ✅ Données pré-traitées")
    st.dataframe(df)

    # Option de téléchargement
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Télécharger les données nettoyées", csv, file_name="donnees_traitees.csv", mime="text/csv")
else:
    st.info("Veuillez sélectionner des colonnes à traiter.")
