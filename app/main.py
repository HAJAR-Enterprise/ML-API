from flask import Flask, request, jsonify
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import tensorflow as tf
import numpy as np
import logging

from utils import (
    normalize_unicode,
    clean_text,
    replace_slang,
    join_spaced_letters,
    load_slang_dictionary
)

MODEL_NAME = "fhru/indobert-judi-online-2"
CACHE_DIR = "/root/.cache/huggingface"

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IndoBERT-API")

try:
    logger.info("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
    model = TFAutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
    slang_dict = load_slang_dictionary()
    logger.info("Model and tokenizer loaded successfully.")
except Exception as e:
    logger.exception("Failed to load model/tokenizer.")
    raise RuntimeError("Model initialization failed") from e

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "IndoBERT Judi Online Classifier API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of comment objects."}), 400

        if not all("commentId" in item and "text" in item for item in data):
            return jsonify({"error": "Each item must contain 'commentId' and 'text'."}), 400

        comment_ids = []
        cleaned_texts = []

        for item in data:
            comment_ids.append(item["commentId"])
            text = item["text"]

            # Preprocessing pipeline
            text = normalize_unicode(text)
            text = clean_text(text)
            text = join_spaced_letters(text)
            text = replace_slang(text, slang_dict)

            cleaned_texts.append(text)

        # Tokenize
        inputs = tokenizer(cleaned_texts, return_tensors="tf", padding=True, truncation=True)

        # Predict
        outputs = model(inputs)
        probs = tf.nn.softmax(outputs.logits, axis=-1).numpy()
        labels = np.argmax(probs, axis=1)

        label_map = {0: "normal", 1: "judi"}

        results = []
        for i, item in enumerate(data):
            label_id = int(labels[i])
            results.append({
                "commentId": comment_ids[i],
                "text": item["text"],
                "label": label_map[label_id],
                "confidence": round(float(probs[i][label_id]), 4)
            })

        return jsonify(results)

    except Exception as e:
        logger.exception("Prediction failed")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
