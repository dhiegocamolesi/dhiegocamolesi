
import pandas as pd

tabela = pd.read_csv("clientes.csv")

display(tabela)

# Score de crédito = Nota de crédito
# Good = Boa
# Standard = OK
# Poor = Ruim

# Passo 2 - Preparar a base de dados para a Inteligência Artificial
display(tabela.info())

# int -> numero inteiro
# float -> numero com casa decimal
# object -> texto

# LabelEncoder
from sklearn.preprocessing import LabelEncoder

# profissao

# cientista - 1
# bombeiro - 2
# engenheiro - 3
# dentista - 4
# artista - 5
codificador_profissao = LabelEncoder()
tabela["profissao"] = codificador_profissao.fit_transform(tabela["profissao"])


# mix_credito
codificador_credito = LabelEncoder()
tabela["mix_credito"] = codificador_credito.fit_transform(tabela["mix_credito"])

# comportamento_pagamento
codificador_pagamento = LabelEncoder()
tabela["comportamento_pagamento"] = codificador_pagamento.fit_transform(tabela["comportamento_pagamento"])


display(tabela.info())

# Passo 3 - Treinar a Inteligência Artificial -> 
# Criar o modelo: Nota de crédito: Boa, Ok, Ruim

# Arvore de Decisão -> RandomForest
# Nearest Neighbors -> KNN -> Vizinhos Próximos

# importar a IA (Inteligencia Artificial)
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

# criar a IA
modelo_arvoredecisao = RandomForestClassifier()
modelo_knn = KNeighborsClassifier()

# treinar a IA
modelo_arvoredecisao.fit(x_treino, y_treino)
modelo_knn.fit(x_treino, y_treino)

# Passo 4 - Escolher qual o melhor modelo
previsao_arvoredecisao = modelo_arvoredecisao.predict(x_teste)
previsao_knn = modelo_knn.predict(x_teste)

# acurácia
from sklearn.metrics import accuracy_score
display(accuracy_score(y_teste, previsao_arvoredecisao))
display(accuracy_score(y_teste, previsao_knn))

# Passo 5 - Usar o melhor modelo para fazer previsão de novos clientes
# melhor modelo é o modelo_arvoredecisao

# importar os novos clientes para fazer a previsao
tabela_novos_clientes = pd.read_csv("novos_clientes.csv")

# profissao
tabela_novos_clientes["profissao"] = codificador_profissao.transform(
    tabela_novos_clientes["profissao"])


# mix_credito
tabela_novos_clientes["mix_credito"] = codificador_credito.transform(
    tabela_novos_clientes["mix_credito"])

# comportamento_pagamento
tabela_novos_clientes["comportamento_pagamento"] = codificador_pagamento.transform(
    tabela_novos_clientes["comportamento_pagamento"])


display(tabela_novos_clientes)

nova_previsao = modelo_arvoredecisao.predict(tabela_novos_clientes)
display(nova_previsao)






