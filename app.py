import numpy as np
import streamlit as st
from scipy.optimize import linprog

def main():
    st.set_page_config(page_title="Resolução de PPL", layout="wide")
    st.title("Resolução de PPL")

    st.sidebar.header("Entradas de dados")

    st.sidebar.subheader("Função Objetivo")
    num_obj_coef = st.sidebar.number_input("Número de Variáveis:", min_value=1, max_value=10, value=2)
    obj_coef = [st.sidebar.number_input(f"Coeficiente {i+1}:", format="%.2f") for i in range(num_obj_coef)]

    st.sidebar.subheader("Restrições")
    num_restricoes = st.sidebar.number_input("Número de Restrições:", min_value=1, max_value=10, value=2)
    rest = []
    for i in range(num_restricoes):
        rest_coef = [st.sidebar.number_input(f"Coeficiente da Restrição {i+1}, Variável {j+1}:", format="%.2f") for j in range(num_obj_coef)]
        rest.append(rest_coef)

    rhs = [st.sidebar.number_input(f"Lado Direito da Restrição {i+1}:", format="%.2f") for i in range(num_restricoes)]

    st.sidebar.subheader("Tipos de Restrições")
    types = []
    for i in range(num_restricoes):
        types.append(st.sidebar.selectbox(f"Tipo de Restrição {i+1}:", ['<=', '>=', '='], index=0))

    if st.button("Calcular"):
        if not obj_coef or not rest or not rhs or not types:
            st.error("Preencha todos os campos corretamente.")
        else:
            A = []
            b = []
            for i in range(len(rest)):
                if types[i].strip() == '<=':
                    A.append(rest[i])
                    b.append(rhs[i])
                elif types[i].strip() == '>=':
                    A.append([-coef for coef in rest[i]])
                    b.append(-rhs[i])
                elif types[i].strip() == '=':
                    A.append(rest[i])
                    A.append([-coef for coef in rest[i]])
                    b.append(rhs[i])
                    b.append(-rhs[i])

            A = np.array(A)
            b = np.array(b)

            bounds = [(0, None) for _ in range(len(obj_coef))]

            c = [-coef for coef in obj_coef]

            res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

            if res.success:
                optimal_value = -res.fun
                optimal_solution = res.x
                st.success(f"Ponto Ótimo: {optimal_solution}")
                st.success(f"Lucro Ótimo: {optimal_value}")

                shadow_prices = res.slack
                st.success(f"Preços Sombra: {shadow_prices}")
            else:
                st.error("Não foi possível encontrar uma solução viável.")

if __name__ == "__main__":
    main()
