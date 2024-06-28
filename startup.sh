#!/bin/bash

apt-get update

apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

pip install PyAudio==0.2.14

ldconfig

python backend.py

streamlit run app.py --server.port $PORT 
