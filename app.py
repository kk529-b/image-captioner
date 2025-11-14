# app.py

import io

import streamlit as st
from PIL import Image

from caption_model import generate_caption_en, generate_caption_ja


def main() -> None:
    st.set_page_config(
        page_title="Image Captioner",
        page_icon="📷",  # 好きな絵文字に変えてOK
        layout="centered",
    )

    st.title("📷 画像キャプション生成アプリ（英語 & 日本語）")
    st.write(
        "画像をアップロードすると、事前学習済みのモデルを使って、"
        "画像の内容を説明するキャプションを英語と日本語で自動生成します。"
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "画像ファイルをアップロード（JPG / PNG）",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is None:
        st.info("上のボックスから画像をアップロードしてください。")
        return

    # 画像読み込み
    try:
        image_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        st.error(f"画像の読み込みに失敗しました: {e}")
        return

    # 画像プレビュー
    st.subheader("アップロードされた画像")
    st.image(image, use_column_width=True)

    st.markdown("### キャプション生成設定")

    length_option = st.selectbox(
        "キャプションの長さ（目安）",
        ("短め", "普通", "やや長め"),
        index=1,
        help="英語・日本語の最大長をざっくり切り替えます。",
    )

    if length_option == "短め":
        max_len_en = 20
        max_len_ja = 25
    elif length_option == "やや長め":
        max_len_en = 40
        max_len_ja = 60
    else:
        max_len_en = 30
        max_len_ja = 40

    num_beams = st.slider(
        "ビームサーチのビーム数（値を上げると少し賢くなるが遅くなります）",
        min_value=1,
        max_value=5,
        value=3,
    )

    generate_button = st.button("キャプションを生成する")

    if not generate_button:
        return

    caption_en = ""
    caption_ja = ""

    with st.spinner("キャプションを生成中です...（初回は少し時間がかかることがあります）"):
        # 英語キャプション
        try:
            caption_en = generate_caption_en(
                image=image,
                max_length=max_len_en,
                num_beams=num_beams,
            )
        except Exception as e:
            st.error(f"英語キャプション生成中にエラーが発生しました: {e}")

        # 日本語キャプション
        try:
            caption_ja = generate_caption_ja(
                image=image,
                max_length=max_len_ja,
                num_beams=num_beams,
            )
        except Exception as e:
            st.error(f"日本語キャプション生成中にエラーが発生しました: {e}")

    st.markdown("### 生成されたキャプション（English）")
    if caption_en:
        st.success(caption_en)
    else:
        st.info("英語キャプションは生成できませんでした。")

    st.markdown("### 生成されたキャプション（日本語）")
    if caption_ja:
        st.success(caption_ja)
    else:
        st.info("日本語キャプションは生成できませんでした。別の画像で試してください。")


if __name__ == "__main__":
    main()