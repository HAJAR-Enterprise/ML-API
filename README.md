# IndoBERT Judi Online Classifier API

API berbasis Flask untuk klasifikasi komentar berbahasa Indonesia terkait judi online, menggunakan model IndoBERT yang telah di-fine-tune.

## 🚀 Fitur

- Model klasifikasi berbasis IndoBERT
- Preprocessing teks bahasa Indonesia
- REST API sederhana (`/predict`)
- Mengembalikan label dan confidence score
- Siap deploy ke Docker & Google Cloud Run

## 🧠 Model

- **Model**: fhru/indobert-judi-online-2
- **Framework**: TensorFlow 2 + HuggingFace Transformers
- **Arsitektur**: IndoBERT (BERT pretrained untuk Bahasa Indonesia)

## 📁 Struktur Proyek

```
.
├── app/
│   ├── main.py
│   ├── utils.py
│   └── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## ⚙️ Instalasi Lokal

1. **Clone repository**:

   ```bash
   git clone https://github.com/username/indobert-judi-api.git
   cd indobert-judi-api
   ```

2. **Build Docker image**:

   ```bash
   docker build -t indobert-api .
   ```

3. **Jalankan image lokal**:
   ```bash
   docker run -p 8080:8080 indobert-api
   ```

## 📡 API Endpoint

### POST `/predict`

Prediksi apakah komentar mengandung unsur judi online.

#### 📥 Contoh Request

```json
[
  {
    "commentId": "abc123",
    "text": "main slot gacor gampang maxwin"
  },
  {
    "commentId": "xyz789",
    "text": "makasih infonya"
  }
]
```

#### 📤 Contoh Response

```json
[
  {
    "commentId": "abc123",
    "text": "main slot gacor gampang maxwin",
    "label": "judi",
    "confidence": 0.9845
  },
  {
    "commentId": "xyz789",
    "text": "makasih infonya",
    "label": "normal",
    "confidence": 0.9968
  }
]
```

## 🐳 Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
```

## ☁️ Deploy ke Google Cloud Run

1. **Tag dan Push ke Artifact Registry**:

   ```bash
   docker tag indobert-api asia-docker.pkg.dev/PROJECT_ID/REPO_NAME/indobert-api
   docker push asia-docker.pkg.dev/PROJECT_ID/REPO_NAME/indobert-api
   ```

2. **Deploy ke Cloud Run**:
   ```bash
   gcloud run deploy indobert-api \
     --image asia-docker.pkg.dev/PROJECT_ID/REPO_NAME/indobert-api \
     --platform managed \
     --region asia-southeast2 \
     --memory 2Gi \
     --timeout 300 \
     --allow-unauthenticated
   ```

## ✅ Tips Produksi

- Gunakan `gunicorn`, bukan `flask run`
- Unduh model saat build image, bukan saat runtime
