import requests
import unicodedata
from urllib.parse import quote

def remover_acentos(texto):
    if not texto: return ""
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn')

def get_regiao_por_cidade(cidade):
    # Envia sem acento para a API (o IBGE aceita e evita erros de URL)
    busca_limpa = quote(remover_acentos(cidade))
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios?nome={busca_limpa}"
    
    try:
        response = requests.get(url, timeout=10)
        municipios = response.json()
        if not municipios: return None

        selecionado = None
        for m in municipios:
            # Comparamos os dois sem acento para garantir que se achem
            if remover_acentos(m['nome']).lower() == remover_acentos(cidade).lower():
                selecionado = m
                break
        
        if not selecionado: selecionado = municipios[0]

        return {
            "cidade": selecionado.get('nome'), # Ex: "Cuiabá"
            "regiao": selecionado['microrregiao']['mesorregiao']['UF']['regiao']['nome']
        }
    except:
        return None

