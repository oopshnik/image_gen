import streamlit as st
import requests
import subprocess
from urllib.parse import quote
from io import BytesIO

st.set_page_config(page_title="image_gen", page_icon="🎨", layout="wide")

st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px 24px !important;
            border-radius: 10px !important;
            border: none !important;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049 !important;
        }
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            font-size: 16px !important;
        }
        .stCheckbox>div>div {
            font-size: 16px !important;
        }
        .title-text {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            background: -webkit-linear-gradient(left, #ff7eb3, #ff758c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🎨 AI Image Generator</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")

    width = st.slider("Width:", 256, 2048, 1024, step=64)
    height = st.slider("Height:", 256, 2048, 1024, step=64)

    if "seed" not in st.session_state:
        st.session_state.seed = 42  # Default seed
    seed = st.number_input("Seed:", value=st.session_state.seed, min_value=0, step=1)

    model = st.selectbox("Model:", ["flux", "flux-pro", "flux-realism", "flux-anime", "flux-3d", "flux-cablyai", "turbo"], index=0)

    st.subheader("🛠️ Additional Options")
    nologo = st.checkbox("Remove Watermark", value=True)
    private = st.checkbox("Keep image private", value=True)
    enhance = st.checkbox("Enhance prompt", value=True)

    st.subheader("ℹ️ About")
    st.markdown("""
    [![Powered by Pollinations.ai](https://img.shields.io/badge/Powered%20by-Pollinations.ai-blue?style=for-the-badge&logo=appveyor&borderRadius=50)](https://pollinations.ai)  
    [![Source Code](https://img.shields.io/badge/Source%20Code-GitHub-black?style=for-the-badge&logo=github&borderRadius=50)](https://github.com/oopshnik/image_gen)  
    [![Developer](https://img.shields.io/badge/Developer-Contact-green?style=for-the-badge&logo=telegram&borderRadius=50)](https://t.me/pr_ogr)
    """, unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Enter Your Image Prompt</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    prompt = st.text_input("Prompt:", placeholder="A futuristic city at sunset 🌇", label_visibility="collapsed")


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🎨 Generate Image", use_container_width=True):
        if not prompt.strip():
            st.error("❌ Please enter a valid prompt.")
        else:
            encoded_prompt = quote(prompt)
            base_url = "https://image.pollinations.ai/prompt/"
            params = {
                "width": width,
                "height": height,
                "seed": seed,
                "nologo": str(nologo).lower(),
                "private": str(private).lower(),
                "enhance": str(enhance).lower(),
                "model": model,
                "safe": "true"
            }
            url = f"{base_url}{encoded_prompt}?" + "&".join([f"{k}={v}" for k, v in params.items()])

            response = requests.get(url)

            if response.status_code == 200:
                img_bytes = BytesIO(response.content)
                process = subprocess.run(["curl", "-f", "-X", "POST", "-F", "file=@-", "https://0x0.st"],
                        input=img_bytes.getvalue(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if process.returncode == 0:
                    upload_url = process.stdout.decode().strip()


                st.image(response.content, caption=f"✨ Generated Image \n🔗 {upload_url}", use_container_width=True)
                st.success(f"✅ Image generated successfully! Seed used: {seed} | Width: {width} | Height: {height}\n {upload_url}")


            else:
                st.error(f"❌ Failed to generate image. Status code: {response.status_code}")