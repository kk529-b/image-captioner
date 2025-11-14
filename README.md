# 画像キャプション生成アプリ（日本語 & 英語対応）

このアプリは、画像をアップロードすると  
**英語キャプションを BLIP モデルで生成し、  
その結果を機械翻訳して日本語キャプションも表示する Web アプリ**です。

- 英語キャプション生成：BLIP（Salesforce/blip-image-captioning-base）
- 日本語キャプション生成：英語キャプション → 翻訳モデル（Helsinki-NLP/opus-mt-en-jap）
- UI：Streamlit

画像 → 英語キャプション → 日本語キャプション  
という **2段階構成**で動作します。

---

## デモ概要

1. 画像をアップロード  
2. BLIP が英語キャプションを生成  
3. 翻訳モデルが日本語キャプションを生成  
4. 両方を画面に表示

---

## 使用技術（Tech Stack）

- **Python 3.9**
- **Streamlit**
- **PyTorch**
- **Hugging Face Transformers**
- **BLIP**（画像→英語キャプション）
- **MarianMT**（英語→日本語翻訳）

---

## 実行方法

```bash
pip install -r requirements.txt
streamlit run app.py