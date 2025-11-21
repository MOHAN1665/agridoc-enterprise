# import streamlit as st
# from PIL import Image
# import io
# from src.config import Config
# from src.agent import PlantDoctorAgent
# from src.database import OutbreakRegistry
# from fpdf import FPDF

# # Initialize Config
# try:
#     Config.validate()
#     # Initialize Agent
#     agent = PlantDoctorAgent()
#     registry = OutbreakRegistry()
#     status_msg = "System Online 🟢 | AI Agent Active"
# except Exception as e:
#     st.error(f"System Init Failure: {e}")
#     status_msg = "System Offline 🔴"

# # === UI CONFIG ===
# st.set_page_config(page_title="AgriDoc Enterprise", layout="wide", page_icon="🌾")

# # === SIDEBAR ===
# with st.sidebar:
#     st.image("https://www.gstatic.com/images/branding/product/2x/google_cloud_64dp.png", width=50)
#     st.title("Control Center")
#     st.markdown("### 🛡️ Outbreak Monitor")
#     stats = registry.get_recent_stats()
#     if stats:
#         st.dataframe(stats)
#     else:
#         st.info("No active outbreaks logged.")
    
#     st.markdown("---")
#     st.caption(f"Agent: {Config.MODEL_NAME}")
#     language = st.sidebar.selectbox("Select Language", ["English", "Hindi", "Spanish", "Telugu"])

# # === MAIN LAYOUT ===
# st.title("🌾 AgriDoc: Intelligent Plant Pathology Agent")
# st.caption(status_msg)

# col1, col2 = st.columns([4, 6])

# with col1:
#     st.markdown("### 1. Visual Input")
#     uploaded_file = st.file_uploader("Upload Field Sample", type=["jpg", "jpeg", "png"])
    
#     if uploaded_file:
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Sample Preview", use_container_width=True)
            
#             # Process
#             if st.button("🚀 Initialize Agent Analysis", type="primary"):
#                 with st.spinner("Agent is analyzing visual patterns & querying protocols..."):
#                     # Convert to bytes
#                     img_byte_arr = io.BytesIO()
                    
#                     # === FIX STARTS HERE ===
#                     # If the image has an Alpha channel (Like PNG), convert it to RGB first
#                     if image.mode in ("RGBA", "P"):
#                         image = image.convert("RGB")
#                     # === FIX ENDS HERE ===
                    
#                     image.save(img_byte_arr, format='JPEG')
#                     img_bytes = img_byte_arr.getvalue()
                    
#                     # CALL THE AGENT
#                     try:
#                         diagnosis, logged = agent.analyze_and_act(img_bytes)
#                         st.session_state['result'] = diagnosis
#                         st.session_state['logged'] = logged
#                     except Exception as e:
#                         st.error(f"Agent Execution Failed: {e}")

# with col2:
#     st.markdown("### 2. Agent Report")
    
#     if 'result' in st.session_state:
#         report = st.session_state['result']
#         logged = st.session_state['logged']
        
#         # Status Banner
#         if logged:
#             st.success("🚨 CRITICAL THREAT DETECTED: Incident automatically logged to National Registry (Firestore).")
#         else:
#             st.info("✅ ANALYSIS COMPLETE: No critical threat requiring database log.")
            
#         st.markdown("#### Diagnosis & Protocol:")
#         st.write(report)
        
#     else:
#         st.markdown("""
#         *Waiting for input...*
        
#         **Agent Capabilities:**
#         1. **Visual Recognition:** Identifies 300+ crop diseases.
#         2. **Autonomous Logging:** Automatically updates Firestore if severity > High.
#         3. **Protocol Generation:** Suggests organic remediation.
#         """)


import streamlit as st
from PIL import Image
import io
from src.config import Config
from src.agent import PlantDoctorAgent
from src.database import OutbreakRegistry
from fpdf import FPDF

# Initialize Config
try:
    Config.validate()
    agent = PlantDoctorAgent()
    registry = OutbreakRegistry()
    status_msg = "System Online 🟢 | AI Agent Active"
except Exception as e:
    st.error(f"System Init Failure: {e}")
    status_msg = "System Offline 🔴"

# === UI CONFIG ===
st.set_page_config(page_title="AgriDoc Enterprise", layout="wide", page_icon="🌾")

# === PDF HELPER ===
def create_pdf(diagnosis_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Handling unicode/emoji in PDFs is tricky, so we keep it simple for hackathon
    clean_text = diagnosis_text.encode('latin-1', 'replace').decode('latin-1') 
    pdf.multi_cell(0, 10, clean_text)
    return pdf.output(dest="S").encode("latin-1")

# === SIDEBAR ===
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/google_cloud_64dp.png", width=50)
    st.title("Control Center")
    st.markdown("### 🛡️ Outbreak Monitor")
    stats = registry.get_recent_stats()
    if stats:
        st.dataframe(stats)
    else:
        st.info("No active outbreaks logged.")
    
    st.markdown("---")
    st.caption(f"Agent: {Config.MODEL_NAME}")
    # Capture language selection
    language = st.sidebar.selectbox("Select Language", ["English", "Hindi", "Spanish", "Telugu"])

# === MAIN LAYOUT ===
st.title("🌾 AgriDoc: Intelligent Plant Pathology Agent")
st.caption(status_msg)

col1, col2 = st.columns([4, 6])

with col1:
    st.markdown("### 1. Visual Input")
    uploaded_file = st.file_uploader("Upload Field Sample", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Sample Preview", use_container_width=True)
            
            # Process
            if st.button("🚀 Initialize Agent Analysis", type="primary"):
                with st.spinner(f"Agent is analyzing in {language}..."):
                    img_byte_arr = io.BytesIO()
                    
                    # Handle PNG transparency
                    if image.mode in ("RGBA", "P"):
                        image = image.convert("RGB")
                    
                    image.save(img_byte_arr, format='JPEG')
                    img_bytes = img_byte_arr.getvalue()
                    
                    # CALL THE AGENT (PASSING THE LANGUAGE NOW)
                    try:
                        # === FIX: Passing 'language' variable ===
                        diagnosis, logged = agent.analyze_and_act(img_bytes, language)
                        st.session_state['result'] = diagnosis
                        st.session_state['logged'] = logged
                    except Exception as e:
                        st.error(f"Agent Execution Failed: {e}")

with col2:
    st.markdown("### 2. Agent Report")
    
    if 'result' in st.session_state:
        report = st.session_state['result']
        logged = st.session_state['logged']
        
        # Status Banner
        if logged:
            st.success("🚨 CRITICAL THREAT DETECTED: Incident automatically logged to National Registry (Firestore).")
        else:
            st.info("✅ ANALYSIS COMPLETE: No critical threat requiring database log.")
            
        st.markdown("#### Diagnosis & Protocol:")
        st.write(report)
        
        # === PDF BUTTON (Inside the column now) ===
        st.markdown("---")
        pdf_data = create_pdf(report)
        st.download_button(
            label="📄 Download Prescription (PDF)",
            data=pdf_data,
            file_name="agridoc_prescription.pdf",
            mime="application/pdf"
        )
        
    else:
        st.markdown("""
        *Waiting for input...*
        
        **Agent Capabilities:**
        1. **Visual Recognition:** Identifies 300+ crop diseases.
        2. **Autonomous Logging:** Automatically updates Firestore if severity > High.
        3. **Protocol Generation:** Suggests organic remediation.
        """)