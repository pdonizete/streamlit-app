import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection


# Função para calcular o IMC
def calcular_imc(peso, altura):
    return peso / (altura**2)


# Função para determinar a faixa de IMC para adultos
def obter_faixa_imc_adulto(imc):
    if imc < 18.5:
        return "Baixo Peso"
    elif 18.5 <= imc < 24.9:
        return "Normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    elif 30 <= imc < 34.9:
        return "Obesidade Grau I"
    elif 35 <= imc < 39.9:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"


# Função simplificada para crianças/adolescentes
def obter_faixa_imc_crianca(imc, idade, sexo):
    # Exemplo simplificado; tabelas específicas são ideais para crianças
    if idade < 2:
        return "IMC não calculável para menores de 2 anos"
    elif 2 <= idade < 5:
        return "Faixa saudável para crianças"
    else:
        return obter_faixa_imc_adulto(imc)


# Função para criar o gráfico de velocímetro
def create_gauge(imc):
    # Definindo as faixas de IMC
    categories = {
        "Baixo Peso": (0, 18.5, "blue"),
        "Normal": (18.5, 24.9, "green"),
        "Sobrepeso": (25, 29.9, "yellow"),
        "Obesidade Grau I": (30, 34.9, "orange"),
        "Obesidade Grau II": (35, 39.9, "red"),
        "Obesidade Grau III": (40, 50, "darkred"),
    }

    # Criando a figura
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.axis("off")

    # Adicionando os wedges (fatias) ao gráfico
    wedges = []
    start_angle = -135
    angle_range = 270 / len(categories)

    for category, (start, end, color) in categories.items():
        wedge = Wedge(
            center=(0, 0),
            r=1,
            theta1=start_angle,
            theta2=start_angle + angle_range,
            facecolor=color,
            edgecolor="white",
        )
        wedges.append(wedge)
        start_angle += angle_range

    # Coleção de wedges
    collection = PatchCollection(wedges, match_original=True)
    ax.add_collection(collection)

    # Adicionando a agulha
    angle = np.interp(imc, [0, 50], [-135, 135])
    ax.plot(
        [0, np.cos(np.radians(angle))],
        [0, np.sin(np.radians(angle))],
        color="black",
        lw=3,
    )

    # Adicionando os rótulos das categorias
    start_angle = -135 + angle_range / 2
    for category, (start, end, color) in categories.items():
        angle = start_angle + angle_range * 0.5
        ax.text(
            np.cos(np.radians(angle)) * 1.3,
            np.sin(np.radians(angle)) * 1.3,
            category,
            horizontalalignment="center",
            verticalalignment="center",
        )
        start_angle += angle_range

    # Título
    ax.text(
        0,
        1.4,
        f"IMC: {imc:.1f}",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=16,
        fontweight="bold",
    )

    st.pyplot(fig)


# Interface do Streamlit
st.title("Calculadora de IMC")
st.write("Insira seus dados para calcular o IMC.")

# Input do usuário
nome = st.text_input("Nome")
idade = st.number_input("Idade", min_value=0, max_value=120, value=25)
sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
peso = st.number_input("Peso (kg)", min_value=0.0, max_value=500.0, value=70.0)
altura = st.number_input("Altura (m)", min_value=0.0, max_value=2.5, value=1.70)

if st.button("Calcular IMC"):
    imc = calcular_imc(peso, altura)
    st.write(f"{nome}, seu IMC é: {imc:.2f}")

    if idade >= 18:
        faixa = obter_faixa_imc_adulto(imc)
    else:
        faixa = obter_faixa_imc_crianca(imc, idade, sexo)

    st.write(f"Classificação: {faixa}")

    # Criar e mostrar o gráfico de velocímetro
    create_gauge(imc)
