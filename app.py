import streamlit as st
import json
import os
from datetime import datetime, timedelta, date

# ----------------------------
# Tema Cyberpunk
# ----------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

.stApp {
    background: linear-gradient(180deg,#0d1b3a,#060c24);
    color:#e8f1ff;
}

h1,h2,h3 {
    color:#00f7ff;
}

.block-container {
    background:#111a3d;
    padding:2rem;
    border-radius:12px;
    border:1px solid #00ffff40;
}

label {
    color:white !important;
    font-weight:600 !important;
}

.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stSelectbox label {
    color:white !important;
}

button {
    border-radius:10px !important;
    background:linear-gradient(90deg,#ff00ff,#00ffff) !important;
    color:white !important;
}

/* animação espadas */

@keyframes swordPulse {

0% {transform:scale(1);}
50% {transform:scale(1.3);}
100% {transform:scale(1);}

}

.sword-victory{
text-align:center;
font-size:42px;
animation:swordPulse 1.2s infinite;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Funções salvar/carregar
# ----------------------------

def carregar_dados():

    if os.path.exists("data.json"):
        with open("data.json","r") as f:
            dados=json.load(f)
    else:
        dados={
            "atividades":{},
            "historico":[],
            "conquistas":[],
            "ultima_semana":0
        }

    if "meta_notificada" not in dados:
        dados["meta_notificada"]=False

    if "ultima_semana" not in dados:
        dados["ultima_semana"]=0

    return dados


def salvar_dados(dados):

    with open("data.json","w") as f:
        json.dump(dados,f)

# ----------------------------
# Interface
# ----------------------------

st.title("🎮 DATAQUEST RPG")

dados = carregar_dados()

nome = st.text_input("Nome do jogador")

if nome:

    atividades = dados.get("atividades",{})
    historico = dados.get("historico",[])
    conquistas = dados.get("conquistas",[])
    semanas_concluidas = dados.get("ultima_semana",0)

    st.success(f"Bem-vindo, {nome}")

    # ----------------------------
    # Cálculos gerais
    # ----------------------------

    xp_total = sum(atividades.values())

    minutos_total = xp_total * 25
    horas = minutos_total // 60
    minutos_restantes = minutos_total % 60

    # ----------------------------
    # Semana atual
    # ----------------------------

    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())

    xp_semana_atual = 0

    for registro in historico:

        data_registro = datetime.strptime(registro["data"], "%Y-%m-%d").date()

        if data_registro >= inicio_semana:
            xp_semana_atual += registro["xp"]

    xp_meta = 60
    xp_percent = min(int((xp_semana_atual / xp_meta)*100),100)

    # ----------------------------
    # Nível do herói
    # ----------------------------

    nivel_heroi = xp_total // 60 + 1

    # ----------------------------
    # Patentes
    # ----------------------------

    if nivel_heroi <= 2:
        patente = "Iniciante"
        estrelas = 1
    elif nivel_heroi <= 4:
        patente = "Aprendiz"
        estrelas = 2
    elif nivel_heroi <= 6:
        patente = "Estudioso"
        estrelas = 3
    elif nivel_heroi <= 8:
        patente = "Analista"
        estrelas = 4
    elif nivel_heroi <= 10:
        patente = "Especialista"
        estrelas = 5
    else:
        patente = "Mestre"

    estrelas_visuais = "🌟"*estrelas + "🔒"*(6-estrelas)

    # ----------------------------
    # Sistema de conquistas
    # ----------------------------

    novas_conquistas=[]

    if xp_total>=3 and "Primeira hora" not in conquistas:
        conquistas.append("Primeira hora")
        novas_conquistas.append("Primeira hora")

    if xp_total>=24 and "10 horas" not in conquistas:
        conquistas.append("10 horas")
        novas_conquistas.append("10 horas")

    if xp_total>=100 and "100 XP" not in conquistas:
        conquistas.append("100 XP")
        novas_conquistas.append("100 XP")

    if semanas_concluidas>=5 and "Semana 5" not in conquistas:
        conquistas.append("Semana 5")
        novas_conquistas.append("Semana 5")

    if semanas_concluidas>=10 and "Semana 10" not in conquistas:
        conquistas.append("Semana 10")
        novas_conquistas.append("Semana 10")

    if novas_conquistas:

        dados["conquistas"]=conquistas
        salvar_dados(dados)

        for c in novas_conquistas:
            st.toast(f"🏆 Conquista desbloqueada: {c}")

    # ----------------------------
    # Barra XP CORRIGIDA
    # ----------------------------

    st.markdown("### ⚡ XP DA SEMANA")

    st.markdown(f"""
    <div style="margin-top:20px;margin-bottom:30px">

    <div style="
    position:relative;
    width:100%;
    height:55px;
    background:#060c24;
    border-radius:14px;
    border:2px solid #00ffff;
    overflow:hidden;
    ">

    <div style="
    height:100%;
    width:{xp_percent}%;
    background:linear-gradient(90deg,#00ffff,#ff00ff);
    transition:width 0.4s;
    ">
    </div>

    <div style="
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:bold;
    font-size:20px;
    color:white;
    pointer-events:none;
    ">

    {xp_semana_atual}/60 XP

    </div>

    </div>

    </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # Meta semanal
    # ----------------------------

    if xp_semana_atual>=60 and not dados.get("meta_notificada",False):

        st.markdown("""
        <div class="sword-victory">
        ⚔️ ⚔️ ⚔️
        </div>
        """, unsafe_allow_html=True)

        st.success("Meta semanal concluída!")

        dados["meta_notificada"]=True
        dados["ultima_semana"]+=1

        salvar_dados(dados)

    if hoje.weekday()==0:
        dados["meta_notificada"]=False
        salvar_dados(dados)

    # ----------------------------
    # NOVA MISSÃO
    # ----------------------------

    st.markdown("## ⚡ NOVA MISSÃO")

    tipo = st.selectbox(
        "Área",
        ["DA (Análise de dados)","Inglês","Outros"]
    )

    if tipo == "Outros":
        atividade = st.text_input("Digite a atividade")
    else:
        atividade = tipo

    xp_ganho = st.number_input("XP ganho",min_value=1,value=1)

    data_estudo = st.date_input("Data do estudo", value=date.today(), format="DD-MM-YYYY")

    if st.button("Registrar missão"):

        if atividade.strip() != "":

            if atividade not in atividades:
                atividades[atividade] = 0

            atividades[atividade] += xp_ganho

            historico.append({
                "data": data_estudo.strftime("%Y-%m-%d"),
                "atividade": atividade,
                "xp": xp_ganho
            })

            dados["atividades"] = atividades
            dados["historico"] = historico

            salvar_dados(dados)

            st.toast(f"+{xp_ganho} XP", icon="⭐")

            st.rerun()

    # ----------------------------
    # STATUS
    # ----------------------------

    st.markdown("## 🧬 STATUS")

    st.write(f"XP desta semana: **{xp_semana_atual}/60**")
    st.write(f"Tempo total estudado: **{horas}h {minutos_restantes}min**")
    st.write(f"Nível do Herói: **{nivel_heroi}**")

    # ----------------------------
    # HORAS POR ÁREA
    # ----------------------------

    st.markdown("## 📚 HORAS POR ÁREA")

    if "confirmar_exclusao" not in st.session_state:
        st.session_state.confirmar_exclusao=None

    for atividade,xp in list(atividades.items()):

        minutos=xp*25
        h=minutos//60
        m=minutos%60

        st.write(f"**{atividade}**")
        st.write(f"{h}h {m}min estudados")

        if st.button(f"Excluir {atividade}"):

            st.session_state.confirmar_exclusao=atividade

        if st.session_state.confirmar_exclusao==atividade:

            st.warning(f"Excluir '{atividade}'?")

            col1,col2=st.columns(2)

            with col1:

                if st.button("Sim",key=f"sim_{atividade}"):

                    del atividades[atividade]

                    historico = [h for h in historico if h["atividade"] != atividade]

                    dados["atividades"]=atividades
                    dados["historico"]=historico

                    salvar_dados(dados)

                    st.session_state.confirmar_exclusao=None

                    st.rerun()

            with col2:

                if st.button("Cancelar",key=f"cancelar_{atividade}"):

                    st.session_state.confirmar_exclusao=None

    # ----------------------------
    # PATENTE
    # ----------------------------

    st.markdown("## 🏅 PATENTE")

    st.write(f"**{patente}**")
    st.write(estrelas_visuais)

    # ----------------------------
    # GERENCIAMENTO
    # ----------------------------

    st.markdown("## ⚙️ GERENCIAMENTO")

    if "confirmar_reset" not in st.session_state:
        st.session_state.confirmar_reset=False

    if st.button("Zerar progresso"):

        st.session_state.confirmar_reset=True

    if st.session_state.confirmar_reset:

        st.warning("Tem certeza que deseja apagar tudo?")

        col1,col2=st.columns(2)

        with col1:

            if st.button("Sim, apagar"):

                dados["atividades"]={}
                dados["historico"]=[]
                dados["conquistas"]=[]
                dados["ultima_semana"]=0
                dados["meta_notificada"]=False

                salvar_dados(dados)

                st.session_state.confirmar_reset=False

                st.rerun()

        with col2:

            if st.button("Cancelar"):

                st.session_state.confirmar_reset=False

    # ----------------------------
    # CONQUISTAS
    # ----------------------------

    st.markdown("## 🏆 CONQUISTAS")

    lista=[
        "Primeira hora",
        "10 horas",
        "100 XP",
        "Semana 5",
        "Semana 10"
    ]

    for c in lista:

        if c in conquistas:
            st.write(f"✅ {c}")
        else:
            st.write(f"⬜ {c}")