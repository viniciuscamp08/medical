import openai
from textblob import TextBlob

# Defina sua chave de API do OpenAI aqui
chave_api = ""
openai.api_key = chave_api

# Lista de hospitais em Manaus com links para Google Maps
hospitais_manaus = [
    {"nome": "28 de Agosto", "endereco": "Av. Mário Ypiranga, 1581 - Adrianópolis",
     "link": "https://goo.gl/maps/K9t6FjY5x3U2"},
    {"nome": "João Lúcio", "endereco": "Av. Cosme Ferreira, 3939 - Coroado",
     "link": "https://goo.gl/maps/3kq4q4aKxUT2"},
    {"nome": "Platão Araújo", "endereco": "Av. Autaz Mirim, 6339 - Tancredo Neves",
     "link": "https://goo.gl/maps/XZ8Er6GmQJs"},
    {"nome": "Adriano Jorge", "endereco": "Av. Carvalho Leal, 1786 - Cachoeirinha",
     "link": "https://goo.gl/maps/JcF6XrFjZ2F2"},
    {"nome": "Getúlio Vargas", "endereco": "Rua Tomas de Vila Nova - Praça 14 de Janeiro",
     "link": "https://goo.gl/maps/FVq2F8Zb2zF2"}
]


def enviar_mensagem(mensagem, lista_mensagem):
    """
    Envia uma mensagem para o modelo GPT-3.5-turbo e retorna a resposta.

    Args:
        mensagem (str): A mensagem enviada pelo usuário.
        lista_mensagem (list): A lista de mensagens que mantém o histórico da conversa.

    Returns:
        str: O conteúdo da resposta gerada pelo modelo.
    """
    lista_mensagem.append({"role": "user", "content": mensagem})
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=lista_mensagem,
        )
        return resposta["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None


def filtro_suporte_medico(resposta):
    """
    Verifica se a resposta contém palavras-chave relacionadas a suporte médico.

    Args:
        resposta (str): O conteúdo da resposta gerada pelo modelo.

    Returns:
        bool: True se a resposta contiver palavras-chave médicas, False caso contrário.
    """
    palavras_chave_medicas = [
        "oi", "saúde", "médico", "doença", "tratamento",
        "consulta", "sintomas", "medicamento", "efeitos colaterais", "diagnóstico", "hospital"
    ] 
    

    conteudo = resposta.lower()
    print(f"Conteúdo da resposta: {conteudo}")  # Debug
    return any(palavra_chave in conteudo for palavra_chave in palavras_chave_medicas)


def analise_sentimento(texto):
    """
    Analisa o sentimento de um texto usando TextBlob.

    Args:
        texto (str): O texto a ser analisado.

    Returns:
        float: A polaridade do sentimento, variando de -1 (negativo) a 1 (positivo).
    """
    blob = TextBlob(texto)
    return blob.sentiment.polarity


def processar_resposta(resposta):
    """
    Processa a resposta gerada pelo modelo, verificando suporte médico e analisando o sentimento.

    Args:
        resposta (str): O conteúdo da resposta gerada pelo modelo.
    """
    if resposta is None:
        print("Não foi possível obter uma resposta do serviço.")
        return

    if filtro_suporte_medico(resposta):
        print("Dra Luh:", resposta)
        polaridade = analise_sentimento(resposta)

        if polaridade > 0:
            print("Sentimento: Positivo")
        elif polaridade < 0:
            print("Sentimento: Negativo")
        else:
            print("Sentimento: Neutro")
    else:
        print("Desculpe, não posso fornecer suporte médico neste momento.")


def localizar_hospitais_manaus():
    """
    Retorna uma lista de hospitais em Manaus com links de localização no Google Maps.
    """
    resposta_hospitais = "Aqui estão alguns hospitais em Manaus:\n"
    for hospital in hospitais_manaus:
        resposta_hospitais += f"- [{hospital['nome']}]({hospital['link']}): {hospital['endereco']}\n"
    return resposta_hospitais


def criar_prompt_inicial():
    """
    Cria um prompt inicial para guiar a interação do usuário com o chatbot.

    Returns:
        list: A lista de mensagens iniciais para iniciar a conversa com o chatbot.
    """
    prompt_inicial = [
        {"role": "system", "content": (
            "Você é Dra Luh, uma assistente virtual especializada em fornecer informações sobre saúde. "
            "Você pode responder a perguntas sobre sintomas, medicamentos, tratamentos e consultas médicas. "
            "No entanto, você não pode fornecer diagnósticos médicos ou prescrições. "
            "Por favor, pergunte como posso ajudar ou diga 'sair' para encerrar a conversa."
        )}
    ]
    return prompt_inicial


def main():
    """
    Função principal que gerencia a interação do usuário com o chatbot.
    """
    lista_mensagem = criar_prompt_inicial()
    print("Olá! Eu sou a Dra Luh, sua assistente virtual de saúde. Como posso ajudar você hoje?")

    while True:
        texto = input("Escreva sua mensagem aqui: ")

        if texto.lower() == "sair":
            break

        if "hospital" in texto.lower():
            resposta = localizar_hospitais_manaus()
        else:
            resposta = enviar_mensagem(texto, lista_mensagem)

        print(f"Resposta recebida: {resposta}")  # Debug
        processar_resposta(resposta)


if __name__ == "__main__":
    main()
