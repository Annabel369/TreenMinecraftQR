import os
import qrcode
from PIL import Image

def gerar_qr_com_paleta(nome_arquivo, tipo_paleta):
    cfgPIX = "810924f7-69b3-4116-8d8f-692e4a25c251"
    pasta_destino = "frame"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)

    largura_alvo = 720
    altura_alvo = 730

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=2
    )
    qr.add_data(cfgPIX)
    qr.make(fit=True)

    matriz = qr.get_matrix()
    linhas_qr = len(matriz)
    colunas_qr = len(matriz[0])

    COR_FUNDO = (245, 238, 227)

    # Definição das paletas de 3 cores
    if tipo_paleta == "rosa":
        C_1, C_2, C_3 = (225, 145, 175), (212, 115, 153), (175, 75, 115)
        CANTO_1, CANTO_2, CANTO_3 = (125, 105, 65), (95, 175, 75), (58, 148, 48)
    elif tipo_paleta == "roxo":
        C_1, C_2, C_3 = (195, 145, 225), (175, 115, 212), (135, 75, 170)
        CANTO_1, CANTO_2, CANTO_3 = (125, 105, 65), (95, 175, 75), (58, 148, 48)
    elif tipo_paleta == "vermelho":
        C_1, C_2, C_3 = (230, 95, 80), (218, 68, 59), (175, 40, 35)
        CANTO_1, CANTO_2, CANTO_3 = (125, 105, 65), (95, 175, 75), (58, 148, 48)
    elif tipo_paleta == "outono":
        C_1, C_2, C_3 = (235, 145, 50), (215, 115, 38), (175, 80, 20)
        CANTO_1, CANTO_2, CANTO_3 = (135, 95, 45), (170, 135, 55), (110, 105, 50)

    tamanho_bloco = 18
    offset_x = 77
    offset_y = 140

    img_final = Image.new("RGB", (largura_alvo, altura_alvo), COR_FUNDO)

    def eh_ancora(r, c):
        tam = 7
        if (r < tam + 2 and c < tam + 2) or \
           (r < tam + 2 and c >= colunas_qr - (tam + 2)) or \
           (r >= linhas_qr - (tam + 2) and c < tam + 2):
            return True
        return False

    for r in range(linhas_qr):
        for c in range(colunas_qr):
            if matriz[r][c]:
                if eh_ancora(r, c):
                    s_canto = (r * 3 + c * 7) % 3
                    cor = CANTO_1 if s_canto == 0 else (CANTO_2 if s_canto == 1 else CANTO_3)
                else:
                    s_centro = (r + c) % 3
                    cor = C_1 if s_centro == 0 else (C_2 if s_centro == 1 else C_3)

                for x in range(tamanho_bloco):
                    for y in range(tamanho_bloco):
                        px = offset_x + (c * tamanho_bloco) + x
                        py = offset_y + (r * tamanho_bloco) + y
                        if px < largura_alvo and py < altura_alvo:
                            img_final.putpixel((px, py), cor)

    img_final.save(caminho_completo)
    print(f"Gerado: {caminho_completo}")

def main():
    # Mapeamento dos frames centrais e suas respectivas paletas
    alvos = [
        (33, "rosa"),
        (109, "roxo"),
        (192, "vermelho"),
        (417, "outono")
    ]

    for centro, paleta in alvos:
        # Gera de -5 até +5 em relação ao frame central
        for offset in range(-5, 6):
            num_frame = centro + offset
            nome_arquivo = f"frame_{num_frame:04d}.png"
            gerar_qr_com_paleta(nome_arquivo, paleta)

    print("Todos os lotes de 5 para frente e 5 para trás foram gerados com sucesso!")

if __name__ == "__main__":
    main()
