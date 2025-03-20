import csv, json
from tqdm import tqdm

tqdm.pandas(desc="Processing", unit_scale=1000)
header = list()
def read_csv(file_path, header):
    with open(file_path, mode='r', encoding='cp1252') as file:
        reader = csv.DictReader(file, delimiter=';')
        total_rows = 0
        print("Filtering rows...")
        header += list(reader.fieldnames)
        filtered_rows = [row for row in tqdm(reader, desc="Processing file", unit="") \
                         if (total_rows := total_rows + 1) \
                            and row['COD_ORG_LOTACAO'] == '45205'
                            and row['COD_ORG_EXERCICIO'] == '45205']
        print("Done. Filtered rows:", len(filtered_rows), "of", total_rows)      
        return filtered_rows

file_path = '/home/william/Downloads/201301_Servidores_SIAPE/201301_Cadastro.csv'
data = read_csv(file_path, header)
print("Creating info.json...")
info = {
    'header': header,
    'uorg_lotacao': {row['COD_UORG_LOTACAO']: row['UORG_LOTACAO'] for row in data},
    'org_lotacao': {row['COD_ORG_LOTACAO']: row['ORG_LOTACAO'] for row in data},
    'orgsup_lotacao': {row['COD_ORGSUP_LOTACAO']: row['ORGSUP_LOTACAO'] for row in data},
    'atividades': {row['CODIGO_ATIVIDADE']: row['ATIVIDADE'] for row in data},
    'uorg_exercicio': {row['COD_UORG_EXERCICIO']: row['UORG_EXERCICIO'] for row in data},
    'org_exercicio': {row['COD_ORG_EXERCICIO']: row['ORG_EXERCICIO'] for row in data},
    'orgsup_exercicio': {row['COD_ORGSUP_EXERCICIO']: row['ORGSUP_EXERCICIO'] for row in data}
}
print("Done.")
print("Creating servidores info...")
info |= {
    'servidores': {row['NOME']: {
        'descricao_cargo': f"{row['CLASSE_CARGO']}{row['PADRAO_CARGO']} {row['DESCRICAO_CARGO']}",
        'funcao': '',        
        'atividade': row['ATIVIDADE'],
        'cod_atividade': row['CODIGO_ATIVIDADE'],
        'cod_uorg_lotacao': row['COD_UORG_LOTACAO'],
        'cod_uorg_exercicio': row['COD_UORG_EXERCICIO'],
        } | {'funcao': f"{row2['SIGLA_FUNCAO']} {row2['FUNCAO']}" 
            for row2 in data 
            if row['Id_SERVIDOR_PORTAL'] == row2['Id_SERVIDOR_PORTAL']
            and row2['SIGLA_FUNCAO'] != '-1'
        } | {'atividade': f"{row2['CODIGO_ATIVIDADE']} {row2['ATIVIDADE']}"
            for row2 in data 
            if row['Id_SERVIDOR_PORTAL'] == row2['Id_SERVIDOR_PORTAL']
            and row2['CODIGO_ATIVIDADE'] != '-1'
        } | {'cod_atividade': row2['CODIGO_ATIVIDADE']
            for row2 in data 
            if row['Id_SERVIDOR_PORTAL'] == row2['Id_SERVIDOR_PORTAL']
            and row2['CODIGO_ATIVIDADE'] != '-1'
        } for row in tqdm(data, desc="Processing servidores", unit="rows") if row['PADRAO_CARGO'] != '-1'}    
}
print("Done.")
print("Sorting...")
info['servidores'] = dict(sorted(info['servidores'].items(), key=lambda item: item[0]))
print("Done.")
print("Creating complementary info.json...")
info |= {    
    'servidores_em_lotacao_atividades': {f"{y} {x}": {
        x2: f"{y2['descricao_cargo']} {y2['funcao']} {y2['atividade']}"
        for x2, y2 in info['servidores'].items() 
        if x==y2['cod_uorg_lotacao'] and x==y2['cod_uorg_exercicio']} 
        for x, y in info['uorg_lotacao'].items()},
    }
print("Done.")
print("Sorting...")
info['atividades'] = dict(sorted(info['atividades'].items(), key=lambda item: item[1]))
info['servidores_em_lotacao_atividades'] = dict(sorted(info['servidores_em_lotacao_atividades'].items(), key=lambda item: item[0]))
print("Done.")
print("Saving info.json...")
with open('info.json', 'w', encoding='utf8') as file:
    json.dump(info, file, indent=2)
print("Done.")