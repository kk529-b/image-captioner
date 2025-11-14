# caption_model.py

import os
from typing import Tuple

from PIL.Image import Image as PILImage
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------
# ■ APIキー読み込み
# -------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY が .env に設定されていません。")

genai.configure(api_key=GEMINI_API_KEY)

# Gemini Vision モデル
gemini_model = genai.GenerativeModel("gemini-2.5-pro")


def generate_captions(image: PILImage) -> Tuple[str, str]:
    """
    Gemini Vision に画像を渡し、英語と日本語のキャプションを同時生成する。
    """
    prompt = """
You are an AI that explains images.

Please describe the uploaded image in the following two formats:

English:
<One concise English caption>

Japanese:
<One natural Japanese caption>

Follow this exact structure with no extra explanation.
"""

    # google-generativeai は PIL.Image をそのまま受け取れる
    response = gemini_model.generate_content([prompt, image])

    text = (response.text or "").strip()

    en_caption = ""
    ja_caption = ""
    mode = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        lower = line.lower()
        if lower.startswith("english"):
            mode = "en"
            continue
        if lower.startswith("japanese"):
            mode = "ja"
            continue

        if mode == "en":
            en_caption = line
        elif mode == "ja":
            ja_caption = line

    return en_caption, ja_caption