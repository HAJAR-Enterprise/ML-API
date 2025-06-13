# IndoBERT Judi Online API Untuk HAJAR

API berbasis Flask untuk klasifikasi komentar berbahasa Indonesia terkait judi online, menggunakan model IndoBERT yang telah di-fine-tune.

## 🚀 Fitur

- Model klasifikasi berbasis IndoBERT
- Preprocessing teks bahasa Indonesia
- REST API sederhana (`/predict`)
- Mengembalikan label dan confidence score

## 🧠 Model

- **Model**: fhru/indobert-judi-online-2
- **Framework**: TensorFlow + HuggingFace Transformers
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
   git clone https://github.com/HAJAR-Enterprise/ML-API.git
   cd ML_API
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
