import requests, json
from pathlib import Path

def recuperar_csv(url):
    headers = {"chave-api-dados":"3a43ad38c90b4b8e3ba861973ed9f6ad"}
    
    pag=1; response = []; ok = True
    while ok:        
        urlFinal = f"{url}?pagina={pag}"
        print(f"Recuperando página {pag}...")
        requestResponse = requests.get(urlFinal, headers=headers)
        if requestResponse.status_code != 200:
            print(f"Falha ao recuperar a página {pag}. Status code: {requestResponse.status_code}")
            break
        responseatual = requestResponse.json()
        response += responseatual
        ok = len(responseatual) > 0
        pag += 1

    if len(response) > 0:        
        with open(Path('cargos.json'), 'w', encoding='utf8') as file:
            json.dump(response, file, indent=2)

# Exemplo de uso
url = 'https://api.portaldatransparencia.gov.br/api-de-dados/servidores/funcoes-e-cargos'

recuperar_csv(url)