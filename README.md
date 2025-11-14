# 画像キャプション生成アプリ（Gemini Vision：日本語 & 英語対応）

このアプリは、Google Gemini の **Vision モデル**を利用して  
**画像1枚から「英語キャプション」と「日本語キャプション」を同時生成する Web アプリ**です。

- Visionモデル：**Gemini 1.5 Flash（Vision対応）**
- 入力：画像（JPG/PNG）
- 出力：英語キャプション + 日本語キャプション
- UI：Streamlit  
- セキュアな構成：`.env` に API キーを保存し、`.gitignore` で Git 管理外にします

Gemini に画像を直接渡せるため、翻訳モデルや BLIP は不要で  
**高速・高精度・シンプルな構成**になっています。

---

## デモ概要

1. 画像をアップロード  
2. Gemini Vision が英語 & 日本語キャプションを同時生成  
3. Web UI に表示

出力例＜馬の写真を入力＞：

English: A horse and a foal grazing in a meadow.
Japanese: 草原で馬と子馬が草を食べている。


Gemini による自然な文章生成のため、翻訳っぽさのない日本語になります。

---

## 使用技術（Tech Stack）

- **Python 3.9+**
- **Streamlit**（Web UI）
- **google-generativeai**（Gemini Vision API）
- **Pillow**（画像処理）
- **python-dotenv**（環境変数管理）

---

## フォルダ構成

image-captioner/
├─ app.py
├─ caption_model.py
├─ requirements.txt
├─ .gitignore
└─ .env.example

# APIキーの設定方法

このアプリを実行するには **Gemini API キー** が必要です。

### ① Gemini API キーを取得する
1. https://aistudio.google.com/app/apikey  
2. 「Create API Key」をクリック  
3. 生成されたキーをコピー

### ② `.env` を作成し、APIキーを保存

---

# 実行方法

プロジェクト直下で：

```bash
pip install -r requirements.txt
streamlit run app.py