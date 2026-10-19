import os
import sys
import tkinter as tk
from PIL import Image, ImageTk

def main():
    pasta_frames = "frames"
    fps = 30
    delay_padrao_ms = int(1000 / fps)

    if not os.path.exists(pasta_frames):
        print(f"Erro: Pasta '{pasta_frames}' não encontrada.")
        sys.exit(1)

    # Lista os frames existentes (de 1 a 425)
    arquivos = [f"frame_{i:04d}.png" for i in range(1, 426)]
    caminhos = [os.path.join(pasta_frames, f) for f in arquivos if os.path.exists(os.path.join(pasta_frames, f))]

    if not caminhos:
        print("Nenhum frame encontrado em 'cortados/'.")
        sys.exit(1)

    print(f"Carregando {len(caminhos)} frames...")

    root = tk.Tk()
    root.title("Animação QR Code")

    # Carrega o primeiro frame para obter dimensões
    primeira_img = Image.open(caminhos[0])
    largura, altura = primeira_img.size

    canvas = tk.Canvas(root, width=largura, height=altura, bg="black")
    canvas.pack()

    # Precarrega as imagens no formato do Tkinter e guarda o número do frame correspondente
    frames_dados = []
    for p in caminhos:
        # Extrai o número do arquivo (ex: "frame_0033.png" -> 33)
        nome_base = os.path.basename(p)
        num_frame = int(nome_base.split('_')[1].split('.')[0])
        img_tk = ImageTk.PhotoImage(Image.open(p))
        frames_dados.append((num_frame, img_tk))

    indice_atual = 0
    image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=frames_dados[0][1])

    # Frames específicos que devem pausar por 30 segundos cada
    frames_pausa = {4, 108, 191, 416}
    tempo_pausa_ms = 5 * 1000  # 30 segundos em milissegundos

    def atualizar_frame():
        nonlocal indice_atual
        
        # Pega o número do frame atual
        num_frame_atual, _ = frames_dados[indice_atual]

        # Avança para o próximo frame no índice
        indice_atual = (indice_atual + 1) % len(frames_dados)
        
        # Atualiza a imagem exibida na tela
        canvas.itemconfig(image_on_canvas, image=frames_dados[indice_atual][1])

        # Define o tempo de espera: se o frame atual estiver na lista, pausa por 30s, senão usa o padrão (30 fps)
        if num_frame_atual in frames_pausa:
            atraso = tempo_pausa_ms
            print(f"Pausa de 30 segundos no frame_{num_frame_atual:04d}.png")
        else:
            atraso = delay_padrao_ms

        root.after(atraso, atualizar_frame)

    root.bind("<Escape>", lambda e: root.destroy())

    # Inicia a animação com o primeiro atraso
    root.after(delay_padrao_ms, atualizar_frame)
    root.mainloop()

if __name__ == "__main__":
    main()