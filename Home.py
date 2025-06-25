import streamlit as st
from pathlib import Path
from src.classes.file import File

st.set_page_config(page_title="Projet Data Mining", layout="centered")
st.title("📊 Projet Data Mining")
st.subheader("Partie I : Exploration initiale des données")

st.markdown("### 📁 Charger un fichier CSV")
uploaded_file = st.file_uploader("Glissez-déposez votre fichier ou cliquez pour en choisir un", type=["csv"])

if uploaded_file is not None:
    st.success("✅ Fichier uploadé avec succès !")

    st.markdown("### 🛠️ Choix du délimiteur")
    delimiter = st.radio(
        "Quel est le séparateur utilisé dans votre fichier ?",
        options=[",", ";", "\t", "|", " "],
        index=0,
        format_func=lambda x: {
            ",": "Virgule `,`",
            ";": "Point-virgule `;`",
            "\t": "Tabulation `\\t`",
            "|": "Barre verticale `|`",
            " ": "Espace ` `"
        }[x]
    )

    if st.button("📂 Charger les données avec ce délimiteur"):
        try:
            # 🔸 Sauvegarde physique du fichier
            uploads_dir = Path("uploads")
            uploads_dir.mkdir(exist_ok=True)
            saved_path = uploads_dir / uploaded_file.name
            with open(saved_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 🔸 Enregistrer chemin et délimiteur en session
            st.session_state["csv_path"] = str(saved_path)
            st.session_state["delimiter"] = delimiter

            fichier = File(saved_path, delimiter=delimiter)
            stats = fichier.get_stats()
            df = stats["df"]

            st.success("✅ Fichier chargé avec succès !")

            st.markdown("### 🔍 Aperçu du début des données")
            st.dataframe(df.head())

            st.markdown("### 🔎 Aperçu de la fin des données")
            st.dataframe(df.tail())

            st.markdown("### ℹ️ Résumé des données")
            st.write(f"**Nom du fichier :** `{stats['filename']}`")
            st.write(f"**Nombre de lignes :** `{stats['shape']['rows']}`")
            st.write(f"**Nombre de colonnes :** `{stats['shape']['columns']}`")
            st.write("**Colonnes :**", stats["columns"])
            st.write("**Types de données :**", stats["dtypes"])
            st.write("**Valeurs manquantes :**", stats["missing_values"])

            st.markdown("### 📈 Statistiques descriptives")
            st.dataframe(df.describe(include='all'))

        except Exception as e:
            st.error(f"❌ Erreur lors du traitement du fichier : {e}")
else:
    st.info("Veuillez charger un fichier CSV pour commencer.")
