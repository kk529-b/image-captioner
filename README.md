# 📷 Image Captioner App (English & Japanese)

A simple web app that generates **image captions** in **English** and **Japanese**.

- English caption: BLIP (Salesforce/blip-image-captioning-base)
- Japanese caption: English → Japanese translation (Helsinki-NLP/opus-mt-en-jap)
- Web UI: Streamlit

## Demo

Upload an image → generate English caption → translate to Japanese.

## Tech Stack

- **Python 3.9**
- **Streamlit**
- **PyTorch**
- **Hugging Face Transformers**
- **BLIP** (image caption model)
- **MarianMT** (translation model)

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py