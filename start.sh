#!/bin/bash

echo "🚀 Not Alma API Başlatılıyor..."
echo "=================================="

# Python3 kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı. Lütfen Python3'ü yükleyin."
    exit 1
fi

# Bağımlılıkları kontrol et
echo "📦 Bağımlılıklar kontrol ediliyor..."
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "📥 Bağımlılıklar yükleniyor..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Bağımlılıklar yüklenemedi."
        exit 1
    fi
    echo "✅ Bağımlılıklar yüklendi."
else
    echo "✅ Bağımlılıklar mevcut."
fi

# .env dosyası kontrolü
if [ ! -f ".env" ]; then
    echo "⚠️  .env dosyası bulunamadı."
    echo "📝 env.example dosyasını .env olarak kopyalayın ve Firebase bilgilerinizi girin."
    echo "   cp env.example .env"
    echo ""
    echo "🔧 Firebase kurulumu için firebase_setup.md dosyasını inceleyin."
    echo ""
    echo "⚠️  Firebase konfigürasyonu olmadan API çalışacak ama notes endpoint'leri çalışmayacak."
    echo ""
fi

# Uygulamayı başlat
echo "🚀 API başlatılıyor..."
echo "📖 API Dokümantasyonu: http://localhost:8000/docs"
echo "🔍 Sağlık Kontrolü: http://localhost:8000/health"
echo "🛑 Durdurmak için Ctrl+C kullanın"
echo ""

python3 run.py
