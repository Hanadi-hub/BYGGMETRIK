import streamlit as st
import pandas as pd

# Grundläggande sidinställningar
st.set_page_config(page_title="Byggmetrik Executive - Malmö Stad", layout="wide")

st.title("BYGGMETRIK EXECUTIVE 2026 – MALMÖ STAD")
st.markdown("*Interaktiv LCC & LCA Systemplattform (Fullständig Excel-Replika)*")

st.sidebar.title("Navigering (Flikar)")
menu = st.sidebar.radio("Välj systemvy:", [
    "1. OMSLAG",
    "2. START & INSTÄLLNINGAR",
    "3. RAW_NETTOKALKYL & BIDCON_IMPORT",
    "4. UNDERHÅLLSPLAN",
    "5. LCC_RESULTAT",
    "6. LCA_RESULTAT"
])

if menu == "1. OMSLAG":
    st.header("🌟 OMSLAG – Exekutiv Omslagssida")
    st.markdown("Välkommen till Byggmetrik-plattformen för Malmö Stad.")
    
    st.subheader("Projektinformation (Projektdata)")
    
    # Projektdatafält
    project_name = st.text_input("Projektnamn", "Exempelprojekt Malmö")
    project_manager = st.text_input("Projektledare", "Eng. Hanadi Taki")
    project_budget = st.number_input("Projektbudget (SEK)", value=1000000, step=50000)
    
    st.success(f"Vald projektinformation har sparats för: {project_name}")

elif menu == "2. START & INSTÄLLNINGAR":
    st.header("⚙️ START & INSTÄLLNINGAR")
    st.markdown("Projektinställningar och grundläggande parametrar.")

elif menu == "3. RAW_NETTOKALKYL & BIDCON_IMPORT":
    st.header("📁 Bidcon Import & QA")
    
    # Uppladdning av flera Bidcon-filer
    uploaded = st.file_uploader("Ladda upp Bidcon-filer (Excel .xlsx)", accept_multiple_files=True)

    if uploaded:
        if isinstance(uploaded, list):
            dfs = [pd.read_excel(f) for f in uploaded]
            df_imported = pd.concat(dfs, ignore_index=True)
        else:
            df_imported = pd.read_excel(uploaded)
        
        st.success("Bidcon-filer har importerats och lästs in framgångsrikt!")
        st.dataframe(df_imported.head())
    else:
        df_imported = None
        st.info("Vänligen ladda upp Bidcon-filer för att starta.")

elif menu == "4. UNDERHÅLLSPLAN":
    st.header("🛠️ UNDERHÅLLSPLAN")
    st.markdown("Underhållsplan och cykeltider enligt SS-EN 15978.")

elif menu == "5. LCC_RESULTAT":
    st.header("💰 LCC_RESULTAT")
    st.markdown("Livscykelkostnadsresultat (LCC).")

elif menu == "6. LCA_RESULTAT":
    st.header("🌍 LCA_RESULTAT")
    st.markdown("Klimatpåverkan och livscykelanalysresultat (LCA).")

# التوقيع الرسمي للمهندسة هادي في أسفل كل الصفحات
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>BYGGMETRIK Executive 2026 🏢 Malmö Stad | Developed by <b>Eng. Hanadi Taki</b></p>", unsafe_allow_html=True)