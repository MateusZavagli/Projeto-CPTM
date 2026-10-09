#Aplicar apenas se identificarmos os dormentes com QR CODE

#Lembrar de instalar a biblioteca no terminal: pip install "qrcode[pil]"
import qrcode
import os

def gerarQrCode():
    while True:
        print("\n------  Gerar QrCode para o Dormente  ------")
        codigo_dormente = input("Digite o código do dormente (Ex: Dormente-0001) ou 0 para voltar ao menu: ")
        if codigo_dormente == "0":
            print("Voltando ao menu...")
            break

        imagem = qrcode.make(codigo_dormente)
        nome_arquivo = f"{codigo_dormente}.png"
        destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "QrCodes")
        os.makedirs(destino, exist_ok=True)
        caminho = os.path.join(destino, nome_arquivo)
        imagem.save(caminho)

        print(f"QR Code para {codigo_dormente} gerado com sucesso! Nome do arquivo: {nome_arquivo}")
