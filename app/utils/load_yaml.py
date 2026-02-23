import streamlit as st
import yaml

@st.cache_data
def func_load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        st.secrets
        return config

config = func_load_config()
st.write(config["version_app"])