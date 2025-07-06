# 🧠 Projeto de Modelagem de Risco de Crédito — Desafio Home Credit (Kaggle)

Este projeto foi desenvolvido como solução para o desafio [Home Credit - Credit Risk Model Stability](https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability), 
com o objetivo de prever o risco de inadimplência de clientes com estabilidade entre diferentes períodos de tempo.

---

## 🎯 Objetivos

- Prever inadimplência de clientes com base em dados de crédito, histórico financeiro e perfil socioeconômico
- Garantir **estabilidade temporal** no desempenho do modelo
- Gerar **insights acionáveis** para áreas de risco, concessão e prevenção de perdas

---

## 🛠️ Técnicas e Ferramentas

| Categoria               | Ferramentas & Técnicas                                |
|------------------------|--------------------------------------------------------|
| Linguagem              | Python (Jupyter Notebook)                             |
| Análise de Dados       | Pandas, NumPy, Seaborn, Matplotlib                    |
| Modelagem Preditiva    | XGBoost, Scikit-learn, Validação cruzada              |
| Interpretação de Modelos | SHAP (Explainable AI)                                |
| Engenharia de Atributos | Criação e seleção de variáveis, tratamento de nulos  |
| Pipeline               | Organização do processo para reprodutibilidade        |

---

## 📊 Etapas do Projeto

1. **Aquisição e entendimento dos dados**
2. **Análise exploratória (EDA)** para identificar padrões e problemas
3. **Limpeza e transformação de dados** (feature engineering, encoding, imputação)
4. **Modelagem preditiva com XGBoost**, com ajuste de hiperparâmetros
5. **Validação temporal e análise de estabilidade do modelo**
6. **Explicabilidade com SHAP**, destacando variáveis-chave
7. **Geração de recomendações práticas para negócios**

---

## 📈 Resultados Obtidos

- Modelo com bom desempenho preditivo (ROC AUC competitivo)
- Boa estabilidade temporal entre `train` e `test`
- Interpretação clara dos principais fatores de inadimplência
- Recomendação de variáveis-chave para revisão de política de crédito

---

## 📎 Fonte dos Dados

Desafio público no Kaggle:  
🔗 [Home Credit - Credit Risk Model Stability](https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability)

---

## 💼 Aplicações Reais

✔️ Análise de risco de crédito em instituições financeiras  
✔️ Apoio à tomada de decisão para aprovação de empréstimos  
✔️ Explicação regulatória e transparência de modelos (compliance)

---

## 📂 Arquivos

- `home_credit_producao.ipynb`: Notebook principal do projeto

