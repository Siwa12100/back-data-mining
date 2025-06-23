import streamlit as st
import pandas as pd
from pathlib import Path
from src.classes.file import File
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler


st.set_page_config(page_title="Pré-traitement", layout="centered")
st.title("🧹 Partie II : Pré-traitement et nettoyage des données")

# ✅ Vérification des infos nécessaires
if "csv_path" not in st.session_state or "delimiter" not in st.session_state:
    st.warning("Veuillez d'abord charger un fichier dans l'étape 1.")
    st.stop()

csv_path = Path(st.session_state["csv_path"])
delimiter = st.session_state["delimiter"]

# ✅ Affichage des infos de session
st.markdown(f"🗂️ **Fichier chargé :** `{csv_path.name}`")
st.markdown(f"🔣 **Délimiteur :** `{delimiter}`")

# ✅ Chargement du fichier
try:
    fichier = File(csv_path, delimiter=delimiter)
    stats = fichier.get_stats()
    df = stats["df"]

    st.success("✅ Fichier bien chargé.")
    st.markdown(f"📏 **Dimensions :** {df.shape[0]} lignes × {df.shape[1]} colonnes")
    st.markdown(f"🧾 **Colonnes détectées :** {', '.join(df.columns)}")

except Exception as e:
    st.error(f"❌ Erreur lors du chargement du fichier : {e}")
    st.stop()

# ✅ Sélection des colonnes numériques
st.markdown("### 🧪 Sélection des colonnes à traiter")
colonnes_numeriques = df.select_dtypes(include='number').columns.tolist()
colonnes_choisies = st.multiselect("Colonnes numériques à traiter :", colonnes_numeriques)

if colonnes_choisies:
    df_avant = df.copy()

    st.markdown("### 🧱 Gestion des valeurs manquantes")
    methode_na = st.selectbox(
        "Méthode de traitement :",
        [
            "Supprimer les lignes",
            "Supprimer les colonnes",
            "Remplir par la moyenne",
            "Remplir par la médiane",
            "Remplir par le mode",
            "Imputation KNN",
            "Imputation par régression"
        ]
    )


    # ✂️ Suppression des lignes
    if methode_na == "Supprimer les lignes":
        df = df.dropna(subset=colonnes_choisies)

    # ✂️ Suppression des colonnes avec des valeurs manquantes
    elif methode_na == "Supprimer les colonnes":
        colonnes_a_supprimer = [col for col in colonnes_choisies if df[col].isna().any()]
        if colonnes_a_supprimer:
            df = df.drop(columns=colonnes_a_supprimer)
            st.warning(f"🗑️ Colonnes supprimées : {', '.join(colonnes_a_supprimer)}")
        else:
            st.info("✅ Aucune des colonnes sélectionnées ne contient de valeur manquante.")


    # 🔢 Remplir par la moyenne
    elif methode_na == "Remplir par la moyenne":
        for col in colonnes_choisies:
            df[col] = df[col].fillna(df[col].mean())

    # 🔢 Remplir par la médiane
    elif methode_na == "Remplir par la médiane":
        for col in colonnes_choisies:
            df[col] = df[col].fillna(df[col].median())

    # 🔢 Remplir par le mode
    elif methode_na == "Remplir par le mode":
        for col in colonnes_choisies:
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode[0])

    # 🤖 Imputation par KNN
    elif methode_na == "Imputation KNN":
        from sklearn.impute import KNNImputer
        imputer = KNNImputer(n_neighbors=3)
        df[colonnes_choisies] = imputer.fit_transform(df[colonnes_choisies])

    # 🔄 Imputation par régression
    elif methode_na == "Imputation par régression":
        from sklearn.experimental import enable_iterative_imputer  # noqa
        from sklearn.impute import IterativeImputer
        imputer = IterativeImputer(random_state=0)
        df[colonnes_choisies] = imputer.fit_transform(df[colonnes_choisies])

    # 📊 Aperçu avant/après
    with st.expander("📊 Aperçu des valeurs manquantes avant/après"):
        avant = df_avant[colonnes_choisies].isna().sum()
        apres = df[colonnes_choisies].isna().sum()
        comparaison = pd.DataFrame({
            "Avant traitement": avant,
            "Après traitement": apres
        })
        st.dataframe(comparaison)

    st.success(f"✅ Traitement des valeurs manquantes appliqué avec la méthode : **{methode_na}**")
# 📈 Normalisation des données
st.markdown("### ⚖️ Normalisation des colonnes")
normalisation = st.selectbox(
    "Méthode de normalisation :",
    [
        "Aucune",
        "Min-Max (0 → 1)",
        "Z-score (moyenne 0, écart-type 1)",
        "RobustScaler (par médiane et IQR)"
    ]
)

if normalisation != "Aucune":
    scaler = None
    if normalisation.startswith("Min-Max"):
        scaler = MinMaxScaler()
    elif normalisation.startswith("Z-score"):
        scaler = StandardScaler()
    elif normalisation.startswith("Robust"):
        scaler = RobustScaler()

    if scaler:
        try:
            df[colonnes_choisies] = scaler.fit_transform(df[colonnes_choisies])
            st.success(f"📊 Normalisation appliquée avec la méthode : **{normalisation}**")
        except Exception as e:
            st.error(f"❌ Erreur lors de la normalisation : {e}")
else:
    st.info("Aucune normalisation appliquée.")

# ✅ Affichage final des données
st.markdown("### ✅ Données pré-traitées")
st.dataframe(df)

# 💾 Téléchargement
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    "💾 Télécharger les données nettoyées",
    csv,
    file_name="donnees_traitees.csv",
    mime="text/csv"
)
