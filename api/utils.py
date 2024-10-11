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







#views:
#!wav to mp3
# def feedback_form_view(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST, request.FILES)  # request.FILES обязательно для файлов
#         if form.is_valid():
#             try:
#                 instance = form.save(commit=False)

#                 # Логирование файла
#                 if 'audio_feedback' in request.FILES:
#                     audio_file = request.FILES['audio_feedback']
#                     print(f"Аудиофайл получен: {audio_file.name}, размер: {audio_file.size}")

#                     # Пробуем сохранить файл
#                     output_filename = save_audio_as_mp3(audio_file, instance)
#                     print(f"Аудиофайл конвертирован в MP3 и сохранен как: {output_filename}")
#                     instance.audio_feedback.name = f'audio_feedbacks/{output_filename}'
#                 else:
#                     print('AUdifile ne poluchen')

#                 instance.save()
#                 print(f"Отзыв сохранен в базе данных с id: {instance.id}")
#                 return redirect('feedback_list_create')
#             except Exception as e:
#                 print(f"Ошибка при сохранении отзыва: {str(e)}")
#                 return render(request, 'feedback_form.html', {'form': form, 'error': str(e)})
#         else:
#             print("Форма не прошла валидацию.")
#     else:
#         form = FeedbackForm()

#     return render(request, 'feedback_form.html', {'form': form})


