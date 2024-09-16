import cv2
import requests
import time  # Импортируем модуль time для задержки

# Адрес API
API_URL = 'http://127.0.0.1:8000/api/check-qr-code/'

# Специальные данные для VIP QR-кода
VIP_QR_DATA = 'vip-&zpkJQ5m!k+K3cBu'

# Функция для получения QR-кода с помощью камеры
def read_qr_code():
    cap = cv2.VideoCapture(0)  # Запуск камеры

    while True:
        ret, frame = cap.read()  # Получение кадра с камеры
        if not ret:
            print("Не удалось запустить камеру")
            break

        # Обнаружение и декодирование QR-кода
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"Данные из QR-кода: {data}")

            # Проверка, является ли этот QR-код VIP-входом
            if data == VIP_QR_DATA:
                print("VIP вход обнаружен!")
                # Можно добавить любую дополнительную логику для VIP
            else:
                send_data_to_api(data)  # Отправка данных QR-кода в API

            time.sleep(3)  # Задержка на 3 секунды

        # Показ изображения, если QR-код найден
        cv2.imshow('Сканирование QR-кода', frame)

        # Если нажать "q", программа завершит работу
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Отключение камеры
    cv2.destroyAllWindows()  # Закрытие всех окон OpenCV

# Функция для отправки данных в API
def send_data_to_api(qr_data):
    try:
        # Отправка данных, полученных из QR-кода (ожидается ID в базе)
        response = requests.post(API_URL, json={"id": qr_data})

        # Проверка ответа от API
        if response.status_code == 200:
            print("Вход разрешен!")
        else:
            print(f"Вход запрещен")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при соединении с API: {e}")

# Основная логика программы
if __name__ == "__main__":
    read_qr_code()  # Запуск функции сканирования QR-кода