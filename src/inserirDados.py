from database import conectar_banco

def iniciarDados():
    while True:
        print("\n------  Inserção de dados dos dormentes  ------")

        entrada = input("Aperte 0 para voltar ao menu ou [ENTER] para prosseguir: ")
        if entrada == '0':
            print("Voltando ao menu...")
            break

        tipoMadeira = input("Insira o tipo de madeira: ")

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