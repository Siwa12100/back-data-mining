import streamlit as st
import pandas as pd
from pathlib import Path
from src.classes.file import File
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

st.set_page_config(page_title="Pré-traitement", layout="centered")
st.title("🧹 Partie II : Pré-traitement et nettoyage des données")

# ✅ Chargement des infos de session
if "csv_path" not in st.session_state or "delimiter" not in st.session_state:
    st.warning("Veuillez d'abord charger un fichier dans l'étape 1.")
    st.stop()

csv_path = Path(st.session_state["csv_path"])
delimiter = st.session_state["delimiter"]

st.markdown(f"🗂️ **Fichier chargé :** `{csv_path.name}`")
st.markdown(f"🔣 **Délimiteur :** `{delimiter}`")

# ✅ Chargement du DataFrame
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
colonnes_numeriques = df.select_dtypes(include="number").columns.tolist()
colonnes_choisies = st.multiselect(
    "Colonnes numériques à traiter :",
    colonnes_numeriques,
    help="Choisissez une ou plusieurs colonnes numériques pour l'imputation et la normalisation."
)

if colonnes_choisies:
    df_avant = df.copy()

    total_na = df[colonnes_choisies].isna().sum().sum()
    if total_na == 0:
        st.info("✅ Aucune valeur manquante dans les colonnes sélectionnées.")
    else:
        st.info(f"Nombre total de valeurs manquantes dans la sélection : **{total_na}**")

    # ✅ Traitement des valeurs manquantes
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
        ],
        help="Sélectionnez la méthode pour traiter les valeurs manquantes. Les méthodes plus sophistiquées peuvent être plus lentes."
    )

    if methode_na == "Supprimer les lignes":
        df = df.dropna(subset=colonnes_choisies)

    elif methode_na == "Supprimer les colonnes":
        colonnes_a_supprimer = [col for col in colonnes_choisies if df[col].isna().any()]
        if colonnes_a_supprimer:
            df = df.drop(columns=colonnes_a_supprimer)
            colonnes_choisies = [col for col in colonnes_choisies if col not in colonnes_a_supprimer]
            st.warning(f"🗑️ Colonnes supprimées : {', '.join(colonnes_a_supprimer)}")
        else:
            st.info("✅ Aucune des colonnes sélectionnées ne contient de valeur manquante.")

    elif methode_na == "Remplir par la moyenne":
        for col in colonnes_choisies:
            df[col] = df[col].fillna(df[col].mean())

    elif methode_na == "Remplir par la médiane":
        for col in colonnes_choisies:
            df[col] = df[col].fillna(df[col].median())

    elif methode_na == "Remplir par le mode":
        for col in colonnes_choisies:
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode[0])

    elif methode_na == "Imputation KNN":
        from sklearn.impute import KNNImputer
        colonnes_incompletes = [col for col in colonnes_choisies if df[col].isna().any()]
        if colonnes_incompletes:
            n_neighbors = st.number_input(
                "Nombre de voisins (K) :",
                min_value=1, max_value=20, value=3,
                help="Le nombre de voisins pour l'imputation KNN."
            )
            imputer = KNNImputer(n_neighbors=int(n_neighbors))
            with st.spinner("Imputation KNN en cours…"):
                arr = imputer.fit_transform(df[colonnes_incompletes])
                df_imputed = pd.DataFrame(arr, columns=colonnes_incompletes, index=df.index)
                df[colonnes_incompletes] = df_imputed
        else:
            st.info("✅ Aucune colonne sélectionnée ne nécessite d'imputation.")

    elif methode_na == "Imputation par régression":
        from sklearn.experimental import enable_iterative_imputer  # noqa
        from sklearn.impute import IterativeImputer
        colonnes_incompletes = [col for col in colonnes_choisies if df[col].isna().any()]
        if colonnes_incompletes:
            max_iter = st.number_input(
                "Nombre maximal d'itérations :",
                min_value=1, max_value=50, value=10,
                help="Le nombre maximal d'itérations pour l'imputation itérative."
            )
            imputer = IterativeImputer(random_state=0, max_iter=int(max_iter))
            with st.spinner("Imputation itérative en cours…"):
                arr = imputer.fit_transform(df[colonnes_incompletes])
                df_imputed = pd.DataFrame(arr, columns=colonnes_incompletes, index=df.index)
                df[colonnes_incompletes] = df_imputed
        else:
            st.info("✅ Aucune colonne sélectionnée ne nécessite d'imputation.")

    # ✅ Comparaison avant/après
    with st.expander("📊 Aperçu des valeurs manquantes avant/après"):
        avant = df_avant[colonnes_choisies].isna().sum()
        apres = df[colonnes_choisies].isna().sum()
        comparaison = pd.DataFrame({
            "Avant traitement": avant,
            "Après traitement": apres
        })
        st.dataframe(comparaison)

    st.success(f"✅ Traitement des valeurs manquantes appliqué ({methode_na})")

    # ✅ Normalisation
    st.markdown("### ⚖️ Normalisation des colonnes")
    normalisation = st.selectbox(
        "Méthode de normalisation :",
        [
            "Aucune",
            "Min-Max (0 → 1)",
            "Z-score (moyenne 0, écart-type 1)",
            "RobustScaler (par médiane et IQR)"
        ],
        help="Choisissez une méthode de normalisation pour les colonnes traitées."
    )

    if normalisation != "Aucune":
        scaler = (
            MinMaxScaler()    if normalisation.startswith("Min-Max") else
            StandardScaler() if normalisation.startswith("Z-score") else
            RobustScaler()
        )
        with st.spinner("Application de la normalisation…"):
            arr = scaler.fit_transform(df[colonnes_choisies])
            df_scaled = pd.DataFrame(arr, columns=colonnes_choisies, index=df.index)
            df[colonnes_choisies] = df_scaled
        st.success(f"📊 Normalisation appliquée : {normalisation}")
    else:
        st.info("Aucune normalisation appliquée.")

else:
    st.info("Sélectionnez d'abord des colonnes numériques pour activer l'imputation et la normalisation.")

# ✅ Aperçu final et export
st.markdown("### ✅ Données pré-traitées")
st.dataframe(df)

# Option : stocker pour future utilisation
st.session_state["df_pretraite"] = df

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "💾 Télécharger les données nettoyées",
    csv,
    file_name="donnees_traitees.csv",
    mime="text/csv"
)
