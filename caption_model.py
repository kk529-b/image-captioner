# caption_model.py

from typing import Optional, Tuple

from PIL.Image import Image as PILImage
import torch
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    VisionEncoderDecoderModel,
    AutoTokenizer,
    AutoImageProcessor,
)

# 英語キャプション用モデル（BLIP）
_EN_MODEL_NAME = "Salesforce/blip-image-captioning-base"

# 日本語キャプション用モデル
_JA_MODEL_NAME = "kumapo/vit-gpt2-ja-image-captioning"

# 英語モデル用
_en_processor: Optional[BlipProcessor] = None
_en_model: Optional[BlipForConditionalGeneration] = None

# 日本語モデル用
_ja_model: Optional[VisionEncoderDecoderModel] = None
_ja_tokenizer: Optional[AutoTokenizer] = None
_ja_image_processor: Optional[AutoImageProcessor] = None

_device: str = "cuda" if torch.cuda.is_available() else "cpu"


def _load_en_model() -> Tuple[BlipProcessor, BlipForConditionalGeneration, str]:
    """
    英語キャプション用 BLIP モデルを 1 回だけロードしてキャッシュする。
    """
    global _en_processor, _en_model

    if _en_processor is None or _en_model is None:
        _en_processor = BlipProcessor.from_pretrained(_EN_MODEL_NAME)
        _en_model = BlipForConditionalGeneration.from_pretrained(
            _EN_MODEL_NAME
        ).to(_device)

    return _en_processor, _en_model, _device


def _load_ja_model() -> Tuple[
    VisionEncoderDecoderModel, AutoTokenizer, AutoImageProcessor, str
]:
    """
    日本語キャプション用モデルを 1 回だけロードしてキャッシュする。
    """
    global _ja_model, _ja_tokenizer, _ja_image_processor

    if _ja_model is None or _ja_tokenizer is None or _ja_image_processor is None:
        _ja_model = VisionEncoderDecoderModel.from_pretrained(_JA_MODEL_NAME).to(
            _device
        )
        _ja_tokenizer = AutoTokenizer.from_pretrained(_JA_MODEL_NAME)
        _ja_image_processor = AutoImageProcessor.from_pretrained(_JA_MODEL_NAME)

    return _ja_model, _ja_tokenizer, _ja_image_processor, _device


def generate_caption_en(
    image: PILImage,
    max_length: int = 30,
    num_beams: int = 3,
) -> str:
    """
    画像から英語キャプションを 1 文生成して返す。
    """
    processor, model, device = _load_en_model()

    inputs = processor(image, return_tensors="pt").to(device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_length=max_length,
            num_beams=num_beams,
        )

    caption = processor.decode(output_ids[0], skip_special_tokens=True)
    return caption.strip()


def generate_caption_ja(
    image: PILImage,
    max_length: int = 40,
    num_beams: int = 4,
) -> str:
    """
    画像から日本語キャプションを 1 文生成して返す。
    """
    model, tokenizer, image_processor, device = _load_ja_model()

    pixel_values = image_processor(
        images=image,
        return_tensors="pt",
    ).pixel_values.to(device)

    with torch.no_grad():
        output_ids = model.generate(
            pixel_values=pixel_values,
            max_length=max_length,
            num_beams=num_beams,
            no_repeat_ngram_size=2,
            early_stopping=True,
        )

    text = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    return text.strip()