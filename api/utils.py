import soundfile as sf
import os

def save_audio_as_mp3(audio_file, instance):
    """Функция для конвертации .wav в .mp3 и сохранения с использованием soundfile."""
    try:
        # Считаем аудиофайл с использованием soundfile
        audio_data, samplerate = sf.read(audio_file)
        output_filename = f'member_{instance.member_id.id}.wav'  # Поменяем на WAV для теста
        output_path = os.path.join('media', 'audio_feedbacks', output_filename)

        # Сохраняем файл в формате WAV (как исходный формат)
        sf.write(output_path, audio_data, samplerate)
        print(f"Аудиофайл сохранен как WAV: {output_path}")

        return output_filename
    except Exception as e:
        print(f"Ошибка при конвертации аудиофайла: {str(e)}")
        raise