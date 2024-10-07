from pydub import AudioSegment
import os

def save_audio_as_mp3(audio_file, instance):
    """Функция для конвертации .wav в .mp3 и сохранения."""
    audio = AudioSegment.from_file(audio_file, format="wav")
    output_filename = f'member_{instance.member_id.id}.mp3'
    output_path = os.path.join('media', 'audio_feedbacks', output_filename)
    audio.export(output_path, format="mp3")
    return output_filename