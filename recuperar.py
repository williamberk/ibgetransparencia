import requests, json
from pathlib import Path

urlbase = 'https://api.portaldatransparencia.gov.br/api-de-dados/'
def recuperar_csv(url: str, arquivosaida: str, info: dict[str, str]):
    headers = {"chave-api-dados":"3a43ad38c90b4b8e3ba861973ed9f6ad"}    
    fulljsonresponse = []
    pag = 1
    while True:
        print("Recuperando página", pag)
        fullinfo = info | {"pagina": pag}
        fullurl = f"{urlbase}{url}?{'&'.join([f"{x}={y}" for x,y in fullinfo.items()])}"
        print(fullurl)
        response = requests.get(fullurl, headers=headers)
        if response.status_code != 200: break
        jsonresponse = response.json()
        if len(jsonresponse) == 0: break
        fulljsonresponse += jsonresponse
        with open(Path(f'{arquivosaida}.json'), 'w', encoding='utf8') as file:
            json.dump(fulljsonresponse, file, indent=2)
        pag += 1
    return fulljsonresponse