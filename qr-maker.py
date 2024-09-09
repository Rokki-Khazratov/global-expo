import qrcode

# Генерация QR-кода с данными билета (например, уникальным идентификатором)
ticket_data = "unique_ticket_id_12345"  # Здесь можно использовать реальные данные билета
img = qrcode.make(ticket_data)

# Сохранение QR-кода в файл
img.save("ticket_qr_code.png")
