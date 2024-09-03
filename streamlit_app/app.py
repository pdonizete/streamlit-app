import streamlit as st

# Título da aplicação
st.title("Minha Primeira Aplicação no Streamlit")

# Texto descritivo
st.write("Bem-vindo à minha primeira aplicação usando Streamlit!")

# Inserindo um número
numero = st.number_input("Escolha um número", min_value=0, max_value=100, value=50)

# Mostrando o resultado
st.write(f"O número escolhido foi: {numero}")

# Gráfico simples
import matplotlib.pyplot as plt

valores = [1, 2, 3, 4, 5]
plt.plot(valores, [v * numero for v in valores])
st.pyplot(plt)
