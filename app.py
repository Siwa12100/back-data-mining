import streamlit as st
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
        options=[",", ";", "\t", "|"],
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
            fichier = File(uploaded_file, delimiter=delimiter)
            stats = fichier.get_stats()
            df = stats["df"]
            
            st.session_state["csv_file"] = uploaded_file
            st.session_state["delimiter"] = delimiter

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
            
            if st.button("➡️ Passer à l'étape 2 : Pré-traitement des données"):
                # st.switch_page("pages/page2.py")
                # st.switch_page("pages/2_Pretraitement_et_nettoyage.py")
                st.switch_page("2_Pretraitement_et_nettoyage")



        except Exception as e:
            st.error(f"❌ Erreur lors du traitement du fichier : {e}")
else:
    st.info("Veuillez charger un fichier CSV pour commencer.")
