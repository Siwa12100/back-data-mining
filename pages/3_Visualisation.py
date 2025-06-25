import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Visualisation", layout="centered")
st.title("📊 Partie III : Visualisation des données nettoyées")

# ✅ Choix de la source des données
st.markdown("### 🚀 Chargement des données")
source = st.radio(
    "Choisissez la source des données à visualiser :",
    ("Réutiliser les données pré-traitées", "Charger un fichier CSV"),
    index=0
)

df = None

if source == "Réutiliser les données pré-traitées":
    if "df_pretraite" in st.session_state:
        df = st.session_state["df_pretraite"]
        st.success("✅ Données pré-traitées chargées depuis la session.")
        st.markdown(f"📏 **Dimensions :** {df.shape[0]} lignes × {df.shape[1]} colonnes")
    else:
        st.warning("⚠️ Aucune donnée pré-traitée disponible en session. Veuillez d'abord passer par la partie II.")
        st.stop()

elif source == "Charger un fichier CSV":
    uploaded = st.file_uploader(
        "Téléchargez un fichier CSV pré-traité",
        type="csv",
        help="Sélectionnez le fichier généré à la fin de la partie II."
    )

    if uploaded is None:
        st.info("Veuillez télécharger un fichier CSV nettoyé pour continuer.")
        st.stop()

    try:
        df = pd.read_csv(uploaded)
        st.success("✅ Fichier chargé avec succès !")
        st.markdown(f"📏 **Dimensions :** {df.shape[0]} lignes × {df.shape[1]} colonnes")
    except Exception as e:
        st.error(f"❌ Impossible de lire le CSV : {e}")
        st.stop()

# ✅ Choix des colonnes numériques
st.markdown("### 🧪 Choix des variables à visualiser")
colonnes_num = df.select_dtypes(include='number').columns.tolist()

if not colonnes_num:
    st.warning("Aucune colonne numérique détectée.")
    st.stop()

select_all = st.checkbox("Tout sélectionner", value=False)

selection = st.multiselect(
    "Choisissez une ou plusieurs colonnes numériques :",
    colonnes_num,
    default=colonnes_num if select_all else None,
    help="Explorez la distribution ou détectez les outliers dans vos colonnes numériques."
)

if not selection:
    st.info("Sélectionnez au moins une colonne pour afficher les graphiques.")
    st.stop()

# ✅ Type de graphique
st.markdown("### 📈 Type de graphique")
graphique = st.radio(
    "Sélectionnez le type de visualisation :",
    ("Histogramme", "Boîte à moustaches"),
    index=0,
    help="Histogramme pour la distribution, boîte à moustaches pour détecter les valeurs aberrantes."
)

# ✅ Génération des graphiques
for col in selection:
    fig, ax = plt.subplots()
    if graphique == "Histogramme":
        bins = st.slider(
            f"Nombre de bins pour {col}",
            min_value=5,
            max_value=100,
            value=30,
            help="Ajustez le nombre de bins pour l'histogramme."
        )
        ax.hist(df[col].dropna(), bins=bins)
        ax.set_title(f"Histogramme de {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Effectif")
    else:
        ax.boxplot(df[col].dropna(), vert=True)
        ax.set_title(f"Boîte à moustaches de {col}")
        ax.set_ylabel(col)

    st.pyplot(fig)

st.success("🎉 Visualisations générées !")
