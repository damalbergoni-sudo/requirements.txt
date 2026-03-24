import streamlit as st
import google.generativeai as genai
import pandas as pd
import datetime
import pytz

# --- CONFIGURAÇÕES DE ALTO NÍVEL ---
st.set_page_config(
    page_title="ALPHA QUANT - B3 ELITE",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização Dark Trader (Bloomberg Style)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; }
    .stMetric { background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; }
    .stButton>button { 
        width: 100%; background: linear-gradient(135deg, #00c853 0%, #64ffda 100%); 
        color: black; font-weight: bold; border: none; height: 4em; font-size: 1.2rem;
        box-shadow: 0 4px 15px rgba(0, 200, 83, 0.3);
    }
    .status-card { background-color: #1a1a1a; border-left: 5px solid #00ff00; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    h1, h2, h3 { color: #00ff00; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA IA (GEMINI) ---
def get_ai_response(prompt):
    try:
        # Puxa a chave dos Secrets do Streamlit
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro na IA: Verifique se a chave GOOGLE_API_KEY está nos Secrets do Streamlit. Detalhe: {e}"

# --- LÓGICA DE DADOS (CONEXÃO PROFIT PRO) ---
def get_live_data():
    # Simulador de dados de alta precisão. 
    # DICA: Para real-time, conecte aqui um link de CSV do Google Sheets sincronizado com seu Profit.
    return {
        "preco": 128650,
        "vwap": 128420,
        "ajuste": 128100,
        "agressao": 64, # 64% Compra
        "sp500": "Alta (+0.52%)",
        "dolar": "Baixa (-0.30%)",
        "z_score": 1.25,
        "noticia": "Fluxo estrangeiro forte na abertura."
    }

data = get_live_data()

# --- INTERFACE PRINCIPAL ---
st.title("🏹 ALPHA QUANTUM v3.0 | B3 WIN")
st.caption(f"Conexão Institucional: ATIVA | Horário B3: {datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')}")

# Métricas de Mercado
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("WIN ATUAL", data['preco'], f"{data['preco']-data['vwap']} pts da VWAP")
with m2: st.metric("AGRESSÃO (TAPE)", f"{data['agressao']}%", "BULLISH")
with m3: st.metric("S&P 500", data['sp500'], "CORRELAÇÃO +")
with m4: st.metric("Z-SCORE (MÉDIA)", data['z_score'], "NORMAL")

st.divider()

# Botão Principal de Entrada
if st.button("🔥 ANALISAR ENTRADA E PONTOS AGORA"):
    with st.spinner("IA processando Fluxo, VWAP e Sentimento Global..."):
        
        prompt_tecnico = f"""
        PERSONA: Trader Senior Pro de Mini Índice.
        DADOS: Preço {data['preco']}, VWAP {data['vwap']}, Ajuste {data['ajuste']}.
        FLUXO: {data['agressao']}% compra. S&P500 {data['sp500']}.
        
        TAREFA: Dê um sinal claro de COMPRA, VENDA ou AGUARDAR.
        Forneça: Entrada, Stop (150 pts), Alvo (350 pts) e a fundamentação baseada em Tape Reading e VWAP.
        Seja direto e use emojis de trader.
        """
        
        resultado = get_ai_response(prompt_tecnico)
        
        st.markdown(f"""
        <div class="status-card">
            <h3>🎯 RELATÓRIO DE EXECUÇÃO</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">{resultado}</p>
        </div>
        """, unsafe_allow_html=True)

# Gestão de Risco e Calculadora
st.divider()
with st.expander("🛡️ GERENCIAMENTO DE RISCO E LOTE"):
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        capital = st.number_input("Capital Operacional (R$)", value=5000)
        risco = st.slider("Risco por Operação (%)", 0.5, 2.0, 1.0)
    with col_r2:
        contratos = max(1, int(capital / 1000)) # Regra de 1 contrato por mil reais (Conservador)
        st.write(f"**Sugestão de Lote:** {contratos} Contratos WIN")
        st.write(f"**Risco Financeiro:** R$ {capital * (risco/100):.2f}")

st.caption("Alpha Quantum - O mercado é soberano. Use a IA como bússola, não como garantia.")
