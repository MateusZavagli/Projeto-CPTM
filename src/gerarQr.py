#Aplicar apenas se identificarmos os dormentes com QR CODE

#Lembrar de instalar a biblioteca no terminal: pip install "qrcode[pil]"
import qrcode
import os
from database import conectar_banco

def gerarQrCode():
    while True:
        print("\n------  Gerar QrCode para o Dormente  ------")
        codigo_dormente = input("Digite o código do dormente (Ex: Dormente-0001) ou 0 para voltar ao menu: ")
        if codigo_dormente == "0":
            print("Voltando ao menu...")
            break

        conexao = conectar_banco()
        cursor = conexao.cursor()

        try:
            cursor.execute("""SELECT codigo, tipo_madeira, [comprimento (m)], data_cadastro
                              FROM dbo.Dormentes
                              WHERE codigo = ?""", (codigo_dormente,))
            linha = cursor.fetchone()
        except Exception as erro:
            print(f"\nERRO ao consultar o banco: {erro}")
            continue
        finally:
            cursor.close()
            conexao.close()
 
        if linha is None:
            print(f"\nERRO!!! Dormente {codigo_dormente} não encontrado. Cadastre-o primeiramente (opção 1).")
            continue
 
        codigo, madeira, comprimento, data = linha
 
        texto = (f"Código: {codigo}\n"
                 f"Madeira: {madeira}\n"
                 f"Comprimento: {float(comprimento):.2f} m\n"
                 f"Cadastro: {data}")
 
        imagem = qrcode.make(texto)
        nome_arquivo = f"{codigo_dormente}.png"
        destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "QrCodes")
        os.makedirs(destino, exist_ok=True)
        caminho = os.path.join(destino, nome_arquivo)
        imagem.save(caminho)

        print(f"QR Code para {codigo_dormente} gerado com sucesso! Nome do arquivo: {nome_arquivo}")
