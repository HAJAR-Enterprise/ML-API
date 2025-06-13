FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# PRE-DOWNLOAD IndoBERT
RUN python -c "from transformers import AutoTokenizer, TFAutoModelForSequenceClassification; \
               AutoTokenizer.from_pretrained('fhru/indobert-finetuned-judi'); \
               TFAutoModelForSequenceClassification.from_pretrained('fhru/indobert-finetuned-judi')"

COPY app/ .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "main:app"]
