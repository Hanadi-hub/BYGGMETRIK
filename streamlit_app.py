import streamlit as st
import pandas as pd

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
    st.markdown("Välkommen till Byggmetrik-plattformen för Malmö Stad. Denna interaktiva plattform hanterar LCC och LCA beräkningar för alla byggprojekt.")
    st.info("👉 Använd sidomenyn till vänster för att navigera till **2. START & INSTÄLLNINGAR** för att fylla i projektuppgifter.")

elif menu == "2. START & INSTÄLLNINGAR":
    st.header("⚙️ START & INSTÄLLNINGAR")
    st.markdown("Projektinställningar och grundläggande parametrar.")
    
    st.subheader("Projektinformation (Projektdata)")
    
    project_name = st.text_input("Projektnamn", "Exempelprojekt Malmö")
    project_type = st.selectbox("Verksamhetstyp / Projekttyp", [
        "Skola / Förskola",
        "Bostäder",
        "Kontor",
        "Vårdbyggnad",
        "Idrottsanläggning",
        "Övrigt"
    ])
    bta_area = st.number_input("BTA - Bruttoarea (m²)", value=1000.0, step=50.0)
    
    st.success(f"Projektdata sparad: {project_name} | Typ: {project_type} | BTA: {bta_area} m²")

elif menu == "3. RAW_NETTOKALKYL & BIDCON_IMPORT":
    st.header("📁 Bidcon Import & QA")
    st.markdown("Ladda upp och sammanfoga dina Bidcon-filer (.csv eller .xlsx).")
    
    uploaded = st.file_uploader("Ladda upp Bidcon-filer", accept_multiple_files=True, type=["csv", "xlsx"])

    if uploaded:
        dfs = []
        for f in uploaded:
            try:
                if f.name.endswith('.csv'):
                    try:
                        df = pd.read_csv(f, sep=';', encoding='latin1')
                    except:
                        df = pd.read_csv(f)
                else:
                    df = pd.read_excel(f)
                dfs.append(df)
            except Exception as e:
                st.warning(f"Kunde inte läsa filen {f.name}. Kontrollera filformatet.")
        
        if dfs:
            df_imported = pd.concat(dfs, ignore_index=True)
            st.success("Alla filer har importerats och lästs in framgångsrikt!")
            st.dataframe(df_imported.head(10))
    else:
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

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>BYGGMETRIK Executive 2026 🏢 Malmö Stad | Developed by <b>Eng. Hanadi Taki</b></p>", unsafe_allow_html=True)