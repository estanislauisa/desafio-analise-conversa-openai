import os
import psycopg2
import json
from fastapi import FastAPI, BackgroundTasks
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Carregar variáveis de ambiente
load_dotenv()

# Configurar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inicializar FastAPI
app = FastAPI()

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")


def fetch_messages(session_id):
    """
    Busca todas as mensagens de uma sessão específica do banco de dados.
    """
    logging.info(f"Buscando mensagens para a sessão {session_id}...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Buscar mensagens relacionadas à sessão
        cursor.execute(
            """
            SELECT remote, content
            FROM message
            WHERE session_id = %s
            ORDER BY id ASC
            """,
            (session_id,)
        )
        messages = cursor.fetchall()
        cursor.close()
        conn.close()

        if not messages:
            logging.warning(f"Nenhuma mensagem encontrada para a sessão {session_id}.")
            return []

        logging.info(f"Mensagens encontradas para a sessão {session_id}: {len(messages)} mensagens.")
        
        # Formatar as mensagens no estilo OpenAI
        formatted_messages = [
            {"role": "user" if remote else "assistant", "content": content}
            for remote, content in messages
        ]
        return formatted_messages

    except Exception as e:
        logging.error(f"Erro ao buscar mensagens para a sessão {session_id}: {e}")
        return []


def save_analysis(session_id, analysis):
    """
    Salva a análise no banco de dados.
    """
    logging.info(f"Salvando análise para a sessão {session_id}...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Inserir dados na tabela analysis
        cursor.execute(
            """
            INSERT INTO analysis (
                session_id, satisfaction, summary, improvement, tone,
                positive_points, negative_points, effort_score, resolution_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session_id,
                analysis["satisfaction"],
                analysis["summary"],
                analysis["improvement"],
                analysis["tone"],
                ', '.join(analysis["positive_points"]),
                ', '.join(analysis["negative_points"]),
                analysis["effort_score"],
                analysis["resolution_status"]
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        logging.info(f"Análise salva com sucesso para a sessão {session_id}.")

    except Exception as e:
        logging.error(f"Erro ao salvar análise para a sessão {session_id}: {e}")


def analyze_session(session_id):
    """
    Realiza a análise de uma sessão específica.
    """
    logging.info(f"Iniciando análise para a sessão {session_id}...")
    
    messages = fetch_messages(session_id)
    if not messages:
        logging.warning(f"Análise abortada para a sessão {session_id}: Nenhuma mensagem encontrada.")
        return

    prompt = f"""
    Você é um assistente avançado treinado para analisar conversas de atendimento ao cliente. Sua tarefa é extrair insights úteis e apresentá-los em formato JSON padronizado. 

    Sua análise deve incluir os seguintes campos:

    1. "satisfaction": Nota de satisfação do cliente de 0 a 10. Avalie com base no tom, no atendimento recebido e na resolução do problema.
    2. "summary": Um resumo breve e preciso da conversa, destacando os pontos principais.
    3. "improvement": Sugestões específicas para melhorar a conversa e o atendimento.
    4. "tone": O tom predominante da conversa, como cordial, frustrante, neutro, etc.
    5. "positive_points": Uma lista de interações ou respostas que agradaram o cliente.
    6. "negative_points": Uma lista de interações ou respostas que desagradam o cliente.
    7. "effort_score": Uma pontuação de 0 a 10 que avalie o esforço que o cliente precisou fazer para atingir seu objetivo.
    8. "resolution_status": Indique se o problema foi resolvido ("Resolvido") ou não ("Não Resolvido").

    Retorne exclusivamente no seguinte formato JSON puro (sem comentários ou texto adicional).

    {{
        "satisfaction": (int),
        "summary": (string),
        "improvement": (string),
        "tone": (string),
        "positive_points": (list of strings),
        "negative_points": (list of strings),
        "effort_score": (int),
        "resolution_status": (string)
    }}

    Conversa a ser analisada:
    {messages}
    """

    try:
        # Chamar o modelo da OpenAI
        logging.info(f"Enviando conversa para análise pela OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        result = response.choices[0].message.content

        # Converter para JSON
        analysis = json.loads(result)
        logging.info(f"Análise recebida da OpenAI para a sessão {session_id}: {analysis}")

        # Salvar análise no banco
        save_analysis(session_id, analysis)

    except Exception as e:
        logging.error(f"Erro ao analisar sessão {session_id}: {e}")


@app.post("/analyze/{session_id}")
def analyze(session_id: int, background_tasks: BackgroundTasks):
    """
    Endpoint para iniciar a análise de uma sessão.
    """
    logging.info(f"Recebida solicitação de análise para a sessão {session_id}.")
    background_tasks.add_task(analyze_session, session_id)
    return {"message": "Análise iniciada", "session_id": session_id}
