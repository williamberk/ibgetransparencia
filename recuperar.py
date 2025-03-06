import requests, json
from pathlib import Path

def recuperar_csv(url):
    headers = {"chave-api-dados":"3a43ad38c90b4b8e3ba861973ed9f6ad"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(Path('saida.json'), 'w', encoding='utf8') as file:
            json.dump(response.json(), file, indent=2)
    else:
        print(f"Falha ao recuperar o arquivo. Status code: {response.status_code}")

# Exemplo de uso
url = 'https://api.portaldatransparencia.gov.br/api-de-dados/servidores?cpf=11085702758'

recuperar_csv(url)