from database import conectar_banco
from enum import Enum

'''class Nomes(Enum):
    1 = "Apuleia leiocarpa"
    2 = "Apuleia molaris"
    3 = "Aspidosperma polyneuron"
    4 = "Bowdichia brasiliensis ou Bowdichia spp"
    5 = "Bowdichia nitida"
    6 = "Bowdichia racemosa"
    7 = "Dialium guianense"
    8 = "Diplotropis purpurea"
    9 = "Dipteryx odorata"
    10 = "Dipteryx spp"
    11 = "Enterolobium schomburgkii"
    12 = "Goupia glabra"
    13 = "Hymenaea courbarii"
    14 = "Hymenaea intermedia"
    15 = "Hymenolobium petraeum ou Hymenolobium spp"
    16 = "Mezilaurus itauba"
    17 = "Ocotea neesiana"
    18 = "Tabebuia serratifolia"
    19 = "Angelim Vermelho (Promap - AMV)"
    20 = "Coimal (Dormentes antigos - AMV)"
    21 = "Veneer (Dormentes antigos - AMV)"
    22 = "Astronium graveolens"
'''

def iniciarDados():
    while True:
        print("\n------  Inserção de dados dos dormentes  ------")

        entrada = input("Aperte 0 para voltar ao menu ou [ENTER] para prosseguir: ")
        if entrada == '0':
            print("Voltando ao menu...")
            break

        tipoMadeira = input("Insira o tipo de madeira: ")

        #nome_cientifico = int(input("Insira o nome científico da madeira: "))

        codigo_dormente = input("Insira o código do dormente (Dormente-000X): ")

        data = input("Insira a data de cadastro do dormente (dd/mm/aaaa): ")

        try:
            comprimento_dormente = float(input("Insira o comprimento em metros do dormente: "))
            quant = int(input("Quantidade de dormentes no lote: "))
            
        except ValueError:
            print("\nERRO!!! Insira valores numéricos válidos para comprimento e quantidade.")
            continue

        comando = """INSERT INTO CPTM_Dormentes.dbo.Dormentes(codigo, tipo_madeira, [comprimento (m)], data_cadastro)
                     VALUES
	                    (?, ?, ?, ?)"""
        conexao = conectar_banco()
        cursor = conexao.cursor()

        try:
            cursor.execute(comando, (codigo_dormente, tipoMadeira, comprimento_dormente, data))
            conexao.commit()
            print(f"\nSUCESSO - Dormente {codigo_dormente} de {tipoMadeira} "
                  f"({comprimento_dormente:.2f}m) cadastrado em {data}.")
        except Exception as erro:
            conexao.rollback()
            print(f"\nERRO ao inserir no banco: {erro}")
        finally:
            cursor.close()
            conexao.close()