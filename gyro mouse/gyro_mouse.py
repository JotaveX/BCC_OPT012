import pyautogui
import socket
import json

# Função para mover o mouse com base nos dados do giroscópio
def move_mouse(gyro_data):
    # Reduzir o fator de escala para diminuir a velocidade do movimento
    scaling_factor = 100  # Fator de escala ajustado para reduzir a velocidade

    # Suavização simples (limita as mudanças abruptas)
    smoothing_factor = 0.5  # O valor do fator de suavização (quanto menor, mais suave)
    
    # Escalar os dados de X e Y para movimentos mais visíveis
    x = gyro_data["x"] * scaling_factor
    y = gyro_data["y"] * scaling_factor
    
    # Obter a posição atual do mouse
    current_x, current_y = pyautogui.position()
    
    # Suavizar o movimento do mouse com base nas mudanças anteriores
    new_x = current_x + x * smoothing_factor
    new_y = current_y + y * smoothing_factor
    
    # Garantir que o mouse não saia da tela (limite de posição)
    screen_width, screen_height = pyautogui.size()
    new_x = max(0, min(new_x, screen_width))
    new_y = max(0, min(new_y, screen_height))

    # Mover o mouse para a nova posição
    pyautogui.moveTo(new_x, new_y)

# Função para testar a conexão UDP e receber os dados
def receive_gyro_data():
    UDP_IP = "0.0.0.0"  # Escutando em todas as interfaces (ou "127.0.0.1" para apenas local)
    UDP_PORT = 12345     # Porta de escuta
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind((UDP_IP, UDP_PORT))
        print(f"Conexão estabelecida. Escutando na porta {UDP_PORT}...")
    except Exception as e:
        print(f"Erro ao abrir a conexão UDP: {e}")
        return  # Se não conseguir abrir o socket, retorna sem fazer nada

    while True:
        # Receber os dados
        data, addr = sock.recvfrom(1024)
        print(f"Recebido de {addr}: {data.decode('utf-8')}")  # Mostra os dados recebidos para depuração
        try:
            # Decodificar os dados JSON e passar para o controle do mouse
            gyro_data = json.loads(data.decode("utf-8"))
            print(f"Dados do giroscópio: {gyro_data}")
            move_mouse(gyro_data)
        except json.JSONDecodeError:
            print("Erro ao decodificar os dados recebidos.")

if __name__ == "__main__":
    print("Aguardando dados do giroscópio...")
    receive_gyro_data()
