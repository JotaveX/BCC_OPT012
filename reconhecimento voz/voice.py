import speech_recognition as sr

def recognize_from_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    try:
        text = recognizer.recognize_google(audio, language='pt-BR', show_all=False)
        print("Você disse:", text)
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao requisitar o serviço: {e}")

def recognize_from_file(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='pt-BR', show_all=False)
        print("Transcrição do arquivo:", text)
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio do arquivo.")
    except sr.RequestError as e:
        print(f"Erro ao requisitar o serviço: {e}")

if __name__ == "__main__":
    print("1 - Reconhecer voz do microfone")
    print("2 - Reconhecer voz de um arquivo WAV")
    escolha = input("Escolha uma opção (1 ou 2): ")
    if escolha == "1":
        recognize_from_microphone()
    elif escolha == "2":
        caminho = input("Informe o caminho do arquivo de áudio (WAV): ")
        recognize_from_file(caminho)
    else:
        print("Opção inválida.")