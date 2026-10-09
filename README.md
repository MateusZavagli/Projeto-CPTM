Inicia com Menu e oferece três opções: 
1. para inserir e cadastrar dados de um dormente/lote;
2. para acessar os dados dos dormentes cadastrados;
3. para gerar QrCode com informações do dormente especificado.

Entrada é lida como str(input()). 

Cada opção terá um arquivo.py específico para funcionamento do sistema selecionado.
Todos iniciam com while True para poder rodar mesmo se entrada for inválida e apersentar um erro - feito com try-except ValueError.

Esse é apenas um protótipo do sistema para o projeto da CPTM, focando em estruturar e entender o funcionamento backend.

Para executar:
python src\menu.py (no terminal)

*Observações:
O arquivo .env guarda a configuração local e nunca deve ser commitado.
A geração de QR Code só se aplica se os dormentes forem identificados por QR Code (alternativa: RFID), conforme o plano.