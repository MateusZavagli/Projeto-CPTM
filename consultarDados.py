from database import conectar_banco

def listarDados():
    while True:

        print("\n------  Dados dos dormentes cadastrados  ------")

        entrada = input("Aperte 0 para voltar ao menu ou [ENTER] para prosseguir: \n")
        if entrada == '0':
            print("Voltando ao menu...")
            break

        conexao = conectar_banco()
        cursor = conexao.cursor()

        try:
            cursor.execute("""SELECT id, codigo, tipo_madeira, [comprimento (m)], data_cadastro
                            FROM dbo.Dormentes
                            ORDER BY id""")
            linhas = cursor.fetchall()

            print(f"{'ID':<5}{'Código':<18}{'Tipo de Madeira':<20}{'Comprimento (m)':<18}{'Data':<10}")
            print("-" * 75)

            for linha in linhas:
                id_dormente, codigo, madeira, comprimento, data = linha
                print(f"{id_dormente:<5}{codigo:<18}{madeira:<20}{float(comprimento):<18.2f}{data:<10}")
            print(f"\nTotal: {len(linhas)} dormente(s).")
        except Exception as erro:
            print(f"\nERRO ao consultar o banco: {erro}")
        finally:
            cursor.close()
            conexao.close()