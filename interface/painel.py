import flet as ft
import socket
import threading

# --- CONFIGURAÇÃO DA MÁQUINA (ARCH LINUX EDITION) ---
# Cole o MAC Address do seu HC-05 aqui
MAC_BLUETOOTH = "00:20:04:BC:DD:CA" 
CANAL_BT = 1 # O HC-05 geralmente usa o canal 1 para Serial Port Profile (SPP)
conexao_bt = None # Variável global para o botão conseguir enxergar o rádio

def main(page: ft.Page):
    global conexao_bt
    
    page.title = "Central de Comando"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK 
    
    titulo = ft.Text("EXTRUSORA PET", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    texto_temp = ft.Text("-- °C", size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER)
    anel_progresso = ft.ProgressRing(width=200, height=200, stroke_width=8, color=ft.Colors.AMBER, value=0)
    
    mostrador = ft.Stack([
        anel_progresso,
        ft.Container(content=texto_temp, alignment=ft.Alignment(0, 0), width=200, height=200)
    ])

    texto_status = ft.Text("Status: Aguardando conexão...", size=16, color=ft.Colors.GREY_400)
    texto_log = ft.Text("", size=12, color=ft.Colors.GREEN_400)

    # --- LÓGICA DO BOTÃO VIRTUAL ---
    motor_forcado = False

    def alternar_motor(e):
        nonlocal motor_forcado
        global conexao_bt
        if conexao_bt:
            try:
                # Inverte o estado atual
                motor_forcado = not motor_forcado 
                
                # Se for verdadeiro manda '1', se for falso manda '0'
                comando = b"1" if motor_forcado else b"0" 
                conexao_bt.send(comando) # Dispara o comando pelo rádio

                # Atualiza o visual do botão
                if motor_forcado:
                    botao_acao.text = "PARAR MOTOR (MANUAL)"
                    botao_acao.bgcolor = ft.Colors.RED_700
                else:
                    botao_acao.text = "FORÇAR EXTRUSÃO"
                    botao_acao.bgcolor = ft.Colors.BLUE_700
                
                page.update()
            except Exception as ex:
                texto_log.value = f"> Erro ao enviar comando: {ex}"
                page.update()

    # O Botão em si
    botao_acao = ft.ElevatedButton(
        "FORÇAR EXTRUSÃO",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        on_click=alternar_motor,
        height=50,
        width=250
    )

    # Adiciona tudo na tela, agora com o botão embaixo do mostrador
    page.add(
        titulo, 
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), 
        mostrador, 
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), 
        botao_acao, # <-- O BOTÃO NASCEU AQUI
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), 
        texto_status, 
        texto_log
    )

    def ler_sensores():
        global conexao_bt
        try:
            conexao_bt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            conexao_bt.connect((MAC_BLUETOOTH, CANAL_BT))
            arquivo_serial = conexao_bt.makefile('r', encoding='utf-8')

            texto_status.value = f"🟢 STATUS: CONECTADO ({MAC_BLUETOOTH})"
            texto_status.color = ft.Colors.GREEN
            page.update()

            while True:
                linha = arquivo_serial.readline().strip()
                if linha:
                    if "Temp:" in linha:
                        partes = linha.split(" ")
                        if len(partes) >= 2:
                            temperatura_str = partes[1]
                            texto_temp.value = f"{temperatura_str} °C"
                            
                            temp_int = int(temperatura_str)
                            anel_progresso.value = temp_int / 250.0 
                            
                            if temp_int >= 210:
                                texto_temp.color = ft.Colors.RED_ACCENT
                                anel_progresso.color = ft.Colors.RED_ACCENT
                            else:
                                texto_temp.color = ft.Colors.AMBER
                                anel_progresso.color = ft.Colors.AMBER
                    page.update()
                    
        except Exception as e:
            texto_status.value = f"🔴 ERRO DE CONEXÃO"
            texto_status.color = ft.Colors.RED
            page.update()

    thread_leitura = threading.Thread(target=ler_sensores, daemon=True)
    thread_leitura.start()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)