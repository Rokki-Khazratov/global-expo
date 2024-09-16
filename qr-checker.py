import cv2
import requests
import time  # Importing time module for delay

# API manzili
API_URL = 'http://127.0.0.1:8000/api/check-qr-code/'

# Kamera yordamida QR-kodni olish funksiyasi
def read_qr_code():
    cap = cv2.VideoCapture(0)  # Kamerani ishga tushirish

    while True:
        ret, frame = cap.read()  # Kadrni olish
        if not ret:
            print("Kamera ishga tushmadi")
            break

        # QR-kodni aniqlash va dekodlash
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"QR-kod ma'lumotlari: {data}")
            send_data_to_api(data)  # QR-kodni APIga yuborish
            time.sleep(3)  # 5 soniya kutish

        # QR-kod aniqlangan bo'lsa, tasvirni ko'rsatish
        cv2.imshow('QR kodni o\'qish', frame)

        # Agar "q" tugmasini bossangiz, dastur to'xtaydi
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# API orqali ma'lumotni yuborish funksiyasi
def send_data_to_api(qr_data):
    try:
        # QR-koddan olingan ma'lumotni yuborish (bazaga id yuborilishi kerak)
        response = requests.post(API_URL, json={"id": qr_data})

        # API dan kelgan javobni tekshirish
        if response.status_code == 200:
            print("True")  # Foydalanuvchi mavjud
        elif response.status_code == 404:
            print("False")  # Foydalanuvchi mavjud emas
        else:
            print(f"API xatosi: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"API bilan bog'lanishda xato yuz berdi: {e}")

# Dastur ishlashi
if __name__ == "__main__":
    read_qr_code()  # QR-kodni o'qish va uzluksiz ishlatish