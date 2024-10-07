from pydub import AudioSegment
import os
import logging

logger = logging.getLogger(__name__)

def save_audio_as_mp3(audio_file, instance):
    """Функция для конвертации .wav в .mp3 и сохранения."""
    try:
        logger.info(f"Начало конвертации аудиофайла: {audio_file.name}")

        # Загружаем .wav файл и конвертируем его в .mp3
        audio = AudioSegment.from_file(audio_file, format="wav")
        output_filename = f'member_{instance.member_id.id}.mp3'
        output_path = os.path.join('media', 'audio_feedbacks', output_filename)

        # Сохраняем файл как .mp3
        audio.export(output_path, format="mp3")
        logger.info(f"Аудиофайл успешно сохранен: {output_path}")

        return output_filename
    except Exception as e:
        logger.error(f"Ошибка при конвертации аудиофайла: {str(e)}")
        raise