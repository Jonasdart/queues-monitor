import streamlit.components.v1 as components
import os

# Define location of the packaged frontend build
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")

_component_func = components.declare_component(
    "custom_slider",
    path=build_dir  # Change how to access component by path instead of url
)
