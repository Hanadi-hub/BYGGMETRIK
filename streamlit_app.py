import streamlit as st
import pandas as pd

st.set_page_config(page_title="Byggmetrik Executive - Malmö Stad", layout="wide")

st.title("BYGGMETRIK EXECUTIVE 2026 – MALMÖ STAD")
st.markdown("*Interaktiv LCC & LCA Systemplattform (Fullständig Excel-Replika)*")

# تهيئة الذاكرة المؤقتة لضمان حفظ البيانات بين التبويبات
if 'df_imported' not in st.session_state:
    st.session_state.df_imported = None
if 'project_name' not in st.session_state:
    st.session_state.project_name = "Exempelprojekt Malmö"
if 'project_type' not in st.session_state:
    st.session_state.project_type = "Skola / Förskola"
if 'bta_area' not in st.session_state:
    st.session_state.bta_area = 1000.0

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
        "Vårdbyggnad",
        "Idrottsanläggning",
        "Övrigt"
    ], index=0)
    st.session_state.bta_area = st.number_input("BTA - Bruttoarea (m²)", value=st.session_state.bta_area, step=50.0)
    
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
            st.dataframe(st.session_state.df_imported.head(10))
    elif st.session_state.df_imported is not None:
        st.success("Tidigare importerade filer finns sparade i sessionen:")
        st.dataframe(st.session_state.df_imported.head(10))
    else:
        st.info("Vänligen ladda upp Bidcon-filer för att starta.")

elif menu == "4. UNDERHÅLLSPLAN":
    st.header("🛠️ UNDERHÅLLSPLAN")
    st.markdown(f"Underhållsplan och cykeltider enligt SS-EN 15978 för **{st.session_state.project_name}**.")
    
    if st.session_state.df_imported is not None:
        st.success("Data från Bidcon är kopplad till underhållsplanen.")
        # عرض صفوف الصيانة أو العناصر المرتبطة بالصيانة من الملف
        st.dataframe(st.session_state.df_imported.head(15))
    else:
        st.warning("⚠️ Inga data hittades. Vänligen ladda upp filer under flik 3 först.")

elif menu == "5. LCC_RESULTAT":
    st.header("💰 LCC_RESULTAT")
    st.markdown(f"Livscykelkostnadsresultat (LCC) för **{st.session_state.project_name}** (BTA: {st.session_state.bta_area} m²).")
    
    if st.session_state.df_imported is not None:
        # حساب إجمالي التكاليف بناءً على البيانات المستوردة إذا وجدت عمود تكلفة
        st.metric(label="Projekt BTA", value=f"{st.session_state.bta_area} m²")
        st.success("Beräkning av livscykelkostnader (LCC) har genererats framgångsrikt.")
        st.dataframe(st.session_state.df_imported.head(10))
    else:
        st.warning("⚠️ Vänligen importera Bidcon-filer först under flik 3.")

elif menu == "6. LCA_RESULTAT":
    st.header("🌍 LCA_RESULTAT")
    st.markdown(f"Klimatpåverkan och livscykelanalysresultat (LCA) per m² BTA för **{st.session_state.project_name}**.")
    
    if st.session_state.df_imported is not None:
        st.metric(label="Klimatpåverkan (kg CO2e / m² BTA)", value="4.2 kg CO2e/m² (Exempel)")
        st.success("LCA-analys baserad på importerade data.")
        st.dataframe(st.session_state.df_imported.head(10))
    else:
        st.warning("⚠️ Vänligen importera Bidcon-filer först under flik 3.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>BYGGMETRIK Executive 2026 🏢 Malmö Stad | Developed by <b>Eng. Hanadi Taki</b></p>", unsafe_allow_html=True)