import json
import requests
import hashlib

def requisitar():
    base_url = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=MEU_TOKEN"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return

def armazenar_dados(dados_json):
    with open('answer.json','w') as json_file:
        json.dump(dados_json,json_file)

def descriptografar_mensagem():
    with open('answer.json','r') as json_file:
        dados = json.load(json_file)
        codificacao = json_file.encoding

    texto_criptografado = dados['cifrado']
    n = dados['numero_casas']
    texto_decifrado = []
    for caracter in texto_criptografado:
        if (ord(caracter) <= 122 and ord(caracter) > 97):
            texto_decifrado.append(chr(ord(caracter)-n))
        elif (ord(caracter) == 97):
            texto_decifrado.append(chr((122 % (ord(caracter) - n))+96))
        else:
            texto_decifrado.append(chr(ord(caracter)))
    mensagem = ''.join(texto_decifrado)
    dados['decifrado'] = mensagem

    with open('answer.json','w') as json_file:
        json.dump(dados,json_file)

def resumo_criptografico():
    with open('answer.json','r') as json_file:
        dados = json.load(json_file)
        codificacao = json_file.encoding

    mensagem = dados['decifrado']
    resumo = hashlib.sha1(mensagem.encode(codificacao)).hexdigest()
    dados['resumo_criptografico'] = resumo

    with open('answer.json', 'w') as json_file:
        json.dump(dados, json_file)

def enviar():
    url = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=MEU_TOKEN"
    answer = {'answer': open('answer.json', 'rb')}
    submit = requests.post(url, files=answer)
    print(submit)

if __name__ == '__main__':
    armazenar_dados(requisitar())
    descriptografar_mensagem()
    resumo_criptografico()
    enviar()