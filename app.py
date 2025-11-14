# app.py

import io

import streamlit as st
from PIL import Image

from caption_model import generate_captions


def main() -> None:
    st.set_page_config(
        page_title="Image Captioner (Gemini Vision)",
        page_icon="📷",
        layout="centered",
    )

    st.title("📷 画像キャプション生成アプリ")
    st.write(
        "Gemini Vision を用いて、画像の内容を英語・日本語の両方で説明します。\n"
        "翻訳モデルや BLIP は使用せず、最速＆最自然なキャプションを返します。"
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "画像をアップロードしてください（jpg / png）",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is None:
        st.info("画像をアップロードしてください。")
        return

    # 画像読み込み
    try:
        image_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        st.error(f"画像の読み込みに失敗しました: {e}")
        return

    st.subheader("アップロードされた画像")
    st.image(image, use_column_width=True)

    if not st.button("キャプションを生成する"):
        return

    with st.spinner("Gemini Vision がキャプションを生成中..."):
        caption_en, caption_ja = generate_captions(image)

    st.markdown("### 🇺🇸 英語キャプション")
    st.success(caption_en)

    st.markdown("### 🇯🇵 日本語キャプション")
    st.success(caption_ja)


if __name__ == "__main__":
    main()