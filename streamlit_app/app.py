import streamlit as st
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

# Configuração do Llama
grog_api_key = st.secrets.get("GROQ_API_KEY")

llama_3 = ChatGroq(
    api_key=grog_api_key,
    model="llama3-70b-8192",
    timeout=180,
)

# Título da aplicação
st.title("Aplicação CrewAI com Streamlit")

# Entrada do usuário
user_input = st.text_input("Pergunta:", "Digite sua pergunta")

# Botão de envio
if st.button("Enviar"):
    # Configuração do agente
    agent = Agent(
        role="Assistente",
        goal="Responder perguntas de forma sucinta em até 140 caracteres",
        backstory=(
            "Você é um assistente rápido e direto ao ponto, conhecido por fornecer "
            "respostas claras e concisas que nunca ultrapassam 140 caracteres."
        ),
        llm=llama_3,
        verbose=True,
        memory=True,
    )

    # Configuração da task
    task = Task(
        description=(
            "Responder à pergunta: '{pergunta}'. "
            "A resposta deve ser clara, concisa e não ultrapassar 140 caracteres. "
            "Evite repetições e mantenha a resposta objetiva."
        ),
        expected_output=(
            "Uma resposta clara, direta e com no máximo 140 caracteres para a pergunta: '{pergunta}'."
        ),
        agent=agent,
    )

    # Configuração da crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )

    # Executa a crew
    result = dict(crew.kickoff(inputs={"pergunta": user_input}))

    # Exibe o resultado
    st.write("Resposta do agente:", result["raw"])
