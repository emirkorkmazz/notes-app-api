#!/usr/bin/env python3
"""
Not Alma API Test Scripti
Bu script API'nin temel fonksiyonlarını test eder.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Sağlık kontrolü testi"""
    print("🔍 Sağlık kontrolü test ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Sağlık kontrolü başarılı:", response.json())
            return True
        else:
            print("❌ Sağlık kontrolü başarısız:", response.status_code)
            return False
    except Exception as e:
        print("❌ Bağlantı hatası:", str(e))
        return False

def test_root():
    """Ana endpoint testi"""
    print("\n🔍 Ana endpoint test ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Ana endpoint başarılı:", response.json())
            return True
        else:
            print("❌ Ana endpoint başarısız:", response.status_code)
            return False
    except Exception as e:
        print("❌ Bağlantı hatası:", str(e))
        return False

def test_docs():
    """API dokümantasyonu testi"""
    print("\n🔍 API dokümantasyonu test ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API dokümantasyonu erişilebilir")
            print(f"📖 Swagger UI: {BASE_URL}/docs")
            return True
        else:
            print("❌ API dokümantasyonu erişilemiyor:", response.status_code)
            return False
    except Exception as e:
        print("❌ Bağlantı hatası:", str(e))
        return False

def test_auth_status():
    """Authentication status endpoint testi"""
    print("\n🔍 Authentication status endpoint test ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Authentication status endpoint çalışıyor")
            print(f"📋 Mesaj: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Authentication status endpoint hatası: {response.status_code}")
            return False
    except Exception as e:
        print("❌ Bağlantı hatası:", str(e))
        return False

def test_notes_endpoint():
    """Notes endpoint testi (authentication olmadan)"""
    print("\n🔍 Notes endpoint test ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/notes/get")
        if response.status_code == 401:
            print("✅ Notes endpoint authentication gerektiriyor (beklenen davranış)")
            return True
        elif response.status_code == 200:
            print("⚠️  Notes endpoint authentication olmadan erişilebilir (beklenmeyen)")
            return False
        else:
            print(f"❌ Notes endpoint beklenmeyen yanıt: {response.status_code}")
            return False
    except Exception as e:
        print("❌ Bağlantı hatası:", str(e))
        return False

def test_openapi():
    """OpenAPI schema testi"""
    print("\n🔍 OpenAPI schema test ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            print("✅ OpenAPI schema erişilebilir")
            print(f"📋 API Başlığı: {schema.get('info', {}).get('title', 'N/A')}")
            print(f"📋 API Versiyonu: {schema.get('info', {}).get('version', 'N/A')}")
            return True
        else:
            print("❌ OpenAPI schema erişilemiyor:", response.status_code)
            return False
    except Exception as e:
        print("❌ Bağlantı hatası:", str(e))
        return False

def main():
    """Ana test fonksiyonu"""
    print("🚀 Not Alma API Test Scripti")
    print("=" * 50)
    
    tests = [
        test_health,
        test_root,
        test_docs,
        test_auth_status,
        test_notes_endpoint,
        test_openapi
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Sonuçları: {passed}/{total} başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı! API çalışıyor.")
        print("\n📖 API Dokümantasyonu:")
        print(f"   Swagger UI: {BASE_URL}/docs")
        print(f"   ReDoc: {BASE_URL}/redoc")
        print("\n✨ Yeni Özellikler:")
        print("   ✅ Request modelleri Swagger UI'da görünüyor")
        print("   ✅ Örnek değerler ve açıklamalar eklendi")
        print("   ✅ Detaylı endpoint açıklamaları")
        print("\n🔧 Firebase Kurulumu:")
        print("   Firebase konfigürasyonu için firebase_setup.md dosyasını inceleyin")
        print("   .env dosyasını Firebase bilgilerinizle doldurun")
    else:
        print("⚠️  Bazı testler başarısız. Lütfen uygulamanın çalıştığından emin olun.")
        print("   Uygulamayı başlatmak için: python run.py")

if __name__ == "__main__":
    main()
