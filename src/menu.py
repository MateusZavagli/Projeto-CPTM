from inserirDados import iniciarDados
from consultarDados import listarDados
from gerarQr import gerarQrCode

while True:
    entrada = input("""\n
------  PROJETO CPTM - Dormentes / Plano de Identificação e Inspeção  ------ 

Para começar, digite:
    1. caso você deseja informar dados de dormente ou lote;
    2. caso você deseja acessar os dados dos dormentes e lotes cadastrados.
    3. Gerar QrCode para um dormente.
Para encerrar a aplicação a qualquer momento, digite "-1"
""")
    
    if entrada == "1":
        iniciarDados()    
    elif entrada == "2":
        listarDados()
    elif entrada == "3":
        gerarQrCode()
    elif entrada == "-1":
        print("Sistema finalizado com sucesso!")
        break
    else:
        print("ERRO!!! Entrada inválida")