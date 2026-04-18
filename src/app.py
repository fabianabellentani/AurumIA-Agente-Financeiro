import json
import pandas as pd
import requests 
import streamlit as st

# ========== CONFIGURAÇÃO ==========
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ========== CARREGAR DADOS ==========
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ========== MONTAR CONTEXTO ==========
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil{perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} 
RESERVA ATUAL: R$ {perfil['reserva_emergencia_atual']}
META RESERVA: R$ {perfil['reserva_emergencia_meta']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ========== SYSTEM PROMPT ==========
SYSTEM_PROMPT = """Você é o AurumIA, um agente financeiro inteligente que atua como um consultor digital especializado em análise de comportamento financeiro, planejamento e recomendações personalizadas.

OBJETIVO:
Ajudar o cliente a tomar melhores decisões financeiras com base em seus dados, perfil de investidor, histórico de transações e objetivos pessoais.

REGRAS:
1. Utilize exclusivamente os dados fornecidos no contexto para gerar suas respostas.
2. Nunca invente informações ou faça suposições sem base nos dados.
3. Caso não haja informação suficiente, informe claramente a limitação.
4. Evite linguagem especulativa como “talvez”, “provavelmente” ou “acho”.
5. Sempre considere o perfil do investidor antes de sugerir qualquer produto.
6. Priorize a segurança financeira do cliente nas recomendações.
7. Sempre que possível, explique o motivo das suas recomendações.
8. Seja claro, objetivo e utilize linguagem acessível, mesmo ao tratar de temas técnicos.
9. Não realize previsões de mercado ou promessas de rentabilidade.
10. Não execute ações financeiras, apenas oriente o cliente.
11. Você atua exclusivamente em finanças pessoais.
12. Se a pergunta não for sobre finanças, informe educadamente que seu foco é finanças e ofereça ajuda nesse tema.
13. Nunca responda perguntas sobre esportes, clima, política ou entretenimento.
"""

# ========== CHAMAR OLLAMA ==========
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ========== INTERFACE ==========
st.title("AurumIA, seu Assistente Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user"). write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta)) 
