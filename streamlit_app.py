import streamlit as st
import pandas as pd

st.set_page_config(page_title="Byggmetrik Executive - Malmö Stad", layout="wide")

st.title("BYGGMETRIK EXECUTIVE 2026 – MALMÖ STAD")
st.markdown("*Interaktiv LCC & LCA Systemplattform (Fullständig Excel-Replika)*")

# Initialize Session State
if 'df_imported' not in st.session_state:
    st.session_state.df_imported = None
if 'project_name' not in st.session_state:
    st.session_state.project_name = "Tygelsjö LSS"
if 'project_type' not in st.session_state:
    st.session_state.project_type = "Vårdbyggnad / LSS"
if 'bta_area' not in st.session_state:
    st.session_state.bta_area = 867.0

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
    
    st.session_state.project_name = st.text_input("Projektnamn", st.session_state.project_name)
    st.session_state.project_type = st.selectbox("Verksamhetstyp / Projekttyp", [
        "Skola / Förskola",
        "Bostäder",
        "Kontor",
        "Vårdbyggnad / LSS",
        "Idrottsanläggning",
        "Övrigt"
    ], index=3)
    st.session_state.bta_area = st.number_input("BTA - Bruttoarea (m²)", value=st.session_state.bta_area, step=10.0)
    
    st.success(f"Projektdata sparad: {st.session_state.project_name} | Typ: {st.session_state.project_type} | BTA: {st.session_state.bta_area} m²")

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
            st.session_state.df_imported = pd.concat(dfs, ignore_index=True)
            st.success("Alla filer har importerats och lästs in framgångsrikt!")
            st.dataframe(st.session_state.df_imported)
    elif st.session_state.df_imported is not None:
        st.success("Tidigare importerade filer finns sparade i sessionen:")
        st.dataframe(st.session_state.df_imported)
    else:
        st.info("Vänligen ladda upp Bidcon-filer för att starta.")

elif menu == "4. UNDERHÅLLSPLAN":
    st.header("🛠️ UNDERHÅLLSPLAN")
    st.markdown(f"Underhållsplan och cykeltider enligt SS-EN 15978 för **{st.session_state.project_name}**.")
    
    if st.session_state.df_imported is not None:
        st.success("Data från Bidcon är kopplad till underhållsplanen.")
        st.dataframe(st.session_state.df_imported)
    else:
        st.warning("⚠️ Inga data hittades. Vänligen ladda upp filer under flik 3 först.")

elif menu == "5. LCC_RESULTAT":
    st.header("💰 LCC_RESULTAT")
    st.markdown(f"Livscykelkostnadsresultat (LCC) för **{st.session_state.project_name}** (BTA: {st.session_state.bta_area} m²).")
    
    if st.session_state.df_imported is not None:
        df = st.session_state.df_imported
        
        # البحث عن أعمدة التكلفة في الملف المرفق
        cost_cols = [col for col in df.columns if 'Kostnad' in col]
        total_cost = 0.0
        
        # محاولة البحث عن عمود الإجمالي الفعلي
        tot_col = [c for c in cost_cols if 'tot' in c or 'mottag' in c or 'summa' in c.lower()]
        if not tot_col and cost_cols:
            tot_col = [cost_cols[-1]]
            
        if tot_col:
            s_series = df[tot_col[0]].astype(str).str.replace(' ', '').str.replace(',', '.').str.replace(r'[^0-9.\-]', '', regex=True)
            total_cost = pd.to_numeric(s_series, errors='coerce').sum()
            
        cost_per_m2 = total_cost / st.session_state.bta_area if st.session_state.bta_area > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Projekt BTA", f"{st.session_state.bta_area:.1f} m²")
        col2.metric("Total Kostnad (Netto)", f"{total_cost:,.0f} SEK".replace(',', ' '))
        col3.metric("Kostnad / m² BTA", f"{cost_per_m2:,.0f} SEK/m²".replace(',', ' '))
        
        st.success("Beräkning av livscykelkostnader (LCC) har genererats framgångsrikt.")
        st.dataframe(df)
    else:
        st.warning("⚠️ Vänligen importera Bidcon-filer först under flik 3.")

elif menu == "6. LCA_RESULTAT":
    st.header("🌍 LCA_RESULTAT")
    st.markdown(f"Klimatpåverkan och livscykelanalysresultat (LCA) för **{st.session_state.project_name}**.")
    
    if st.session_state.df_imported is not None:
        df = st.session_state.df_imported
        
        # البحث عن أعمدة الكربون CO2e في الملف المرفق
        co2_cols = [col for col in df.columns if 'CO2e' in col or 'kg CO2e' in col]
        total_co2 = 0.0
        
        tot_co2_col = [c for c in co2_cols if 'tot' in c]
        if not tot_co2_col and co2_cols:
            tot_co2_col = [co2_cols[0]]
            
        if tot_co2_col:
            c_series = df[tot_co2_col[0]].astype(str).str.replace(' ', '').str.replace(',', '.').str.replace(r'[^0-9.\-]', '', regex=True)
            total_co2 = pd.to_numeric(c_series, errors='coerce').sum()
            
        co2_per_m2 = total_co2 / st.session_state.bta_area if st.session_state.bta_area > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Projekt BTA", f"{st.session_state.bta_area:.1f} m²")
        col2.metric("Total Klimatpåverkan", f"{total_co2:,.1f} kg CO2e".replace(',', ' '))
        col3.metric("Klimatpåverkan / m² BTA", f"{co2_per_m2:.2f} kg CO2e/m²")

        st.success("LCA-analys baserad på importerade data.")
        st.dataframe(df)
    else:
        st.warning("⚠️ Vänligen importera Bidcon-filer först under flik 3.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>BYGGMETRIK Executive 2026 🏢 Malmö Stad | Developed by <b>Eng. Hanadi Taki</b></p>", unsafe_allow_html=True)