import streamlit as st
import pandas as pd

# Grundläggande sidinställningar
st.set_page_config(page_title="Byggmetrik Executive - Malmö Stad", layout="wide")

st.title("BYGGMETRIK EXECUTIVE 2026 – MALMÖ STAD")
st.markdown("*Interaktiv LCC & LCA Systemplattform (Fullständig Excel-Replika)*")

# القائمة الجانبية للتنقل بين الأقسام الستة تماماً مثل ملف الإكسل الأصلي
st.sidebar.title("Navigering (Flikar)")
menu = st.sidebar.radio("Välj systemvy:", [
    "1. OMSLAG",
    "2. START & INSTÄLLNINGAR",
    "3. RAW_NETTOKALKYL & BIDCON_IMPORT",
    "4. UNDERHÅLLSPLAN",
    "5. LCC_RESULTAT",
    "6. LCA_RESULTAT"
])

# 1. OMSLAG (صفحة الغلاف)
if menu == "1. OMSLAG":
    st.header("🌟 OMSLAG – Exekutiv Omslagssida")
    st.markdown("Välkommen till Byggmetrik-plattformen för Malmö Stad. Denna plattform ersätter den traditionella Excel-kalkylen för LCC och LCA.")
    st.info("👉 Använd sidomenyn för att navigera till **2. START & INSTÄLLNINGAR** för att registrera ditt projekt.")

# 2. START & INSTÄLLNINGAR (إعدادات المشروع الأساسية)
elif menu == "2. START & INSTÄLLNINGAR":
    st.header("⚙️ START & INSTÄLLNINGAR")
    st.markdown("Projektinställningar och grundläggande parametrar enligt Malmö Stads riktlinjer.")
    
    st.subheader("Projektinformation (Projektdata)")
    
    # حقول إدخال بيانات المشروع (اسم المشروع، نوع النشاط، المساحة BTA)
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

# 3. RAW_NETTOKALKYL & BIDCON_IMPORT (استيراد ملفات Bidcon المتعددة)
elif menu == "3. RAW_NETTOKALKYL & BIDCON_IMPORT":
    st.header("📁 Bidcon Import & QA")
    st.markdown("Importera och sammanfoga flera Bidcon-filer (.xlsx) samtidigt.")
    
    # رفع الملفات المتعددة دفعة واحدة
    uploaded = st.file_uploader("Ladda upp Bidcon-filer (Excel .xlsx)", accept_multiple_files=True, type=["xlsx"])

    if uploaded:
        try:
            if isinstance(uploaded, list):
                dfs = [pd.read_excel(f, engine='openpyxl') for f in uploaded]
                df_imported = pd.concat(dfs, ignore_index=True)
            else:
                df_imported = pd.read_excel(uploaded, engine='openpyxl')
            
            st.success("Bidcon-filer har importerats och lästs in framgångsrikt!")
            st.dataframe(df_imported.head())
        except Exception as e:
            st.error("Ett fel uppstod vid inläsning av filer.")
            st.exception(e)
    else:
        df_imported = None
        st.info("Vänligen ladda upp Bidcon-filer för att starta.")

# 4. UNDERHÅLLSPLAN (خطة الصيانة)
elif menu == "4. UNDERHÅLLSPLAN":
    st.header("🛠️ UNDERHÅLLSPLAN")
    st.markdown("Underhållsplan och cykeltider enligt SS-EN 15978.")
    st.write("Här visas underhållsintervaller och årliga kostnader för projektets komponenter.")

# 5. LCC_RESULTAT (نتائج تكلفة دورة الحياة)
elif menu == "5. LCC_RESULTAT":
    st.header("💰 LCC_RESULTAT")
    st.markdown("Livscykelkostnadsresultat (LCC) för Malmö Stad.")
    st.write("Sammanställning av investeringskostnader, underhåll och restvärde.")

# 6. LCA_RESULTAT (نتائج تحليل دورة الحياة الكربونية)
elif menu == "6. LCA_RESULTAT":
    st.header("🌍 LCA_RESULTAT")
    st.markdown("Klimatpåverkan och livscykelanalysresultat (LCA) per m² BTA.")
    st.write("Analys av växthusgaser (kg CO2e / m² BTA) för byggnadens livscykel.")

# التوقيع الرسمي للمهندسة هنادي في أسفل المنصة
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>BYGGMETRIK Executive 2026 🏢 Malmö Stad | Developed by <b>Eng. Hanadi Taki</b></p>", unsafe_allow_html=True)