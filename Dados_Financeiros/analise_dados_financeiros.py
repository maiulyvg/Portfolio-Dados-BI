# 1 Introdução ao projeto

# 1.1 Importação de Bibliotecas de Python
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
from datetime import datetime
import seaborn  as sns
import locale
from statsmodels.graphics.mosaicplot import mosaic

# 1.2 Acessando arquivos .csv
df_ag = pd.read_csv('/content/agencias.csv')
df_cli = pd.read_csv('/content/clientes.csv')
df_colbag = pd.read_csv('/content/colaborador_agencia.csv')
df_colb = pd.read_csv('/content/colaboradores.csv')
df_cnt = pd.read_csv('/content/contas.csv')
df_prop = pd.read_csv('/content/propostas_credito.csv')
df_tr = pd.read_csv('/content/transacoes.csv')

# 1.3 Criação de um banco de dados relacional usando SQLite
conn = sqlite3.connect ("database.db")
# Inserindos os DataFrame vindos das tabelas .CSV no banco de dados do SQLite
df_ag.to_sql('agencias', conn, if_exists='replace', index=False)
df_cli.to_sql('clientes', conn, if_exists='replace', index=False)
df_colbag.to_sql('colaborador_agencia', conn, if_exists='replace', index=False)
df_colb.to_sql('colaboradores', conn, if_exists='replace', index=False)
df_cnt.to_sql('contas', conn, if_exists='replace', index=False)
df_prop.to_sql('propostas_credito', conn, if_exists='replace', index=False)
df_tr.to_sql('transacoes', conn, if_exists='replace', index=False)

# 1.4 Junção das tabelas do Data Warehouse em uma única tabela usando SQL
# Criação de uma query no projeto do BigQuery juntando as tabelas, excluindo colunas repetidas (com chaves estrangeiras) e com dados sensíveis (cpf, cnpj, email e cep),
# renomeando colunas (que tem título repetido entre as tabelas), concatenando colunas (de primeiro e último nome de clientes e colaboradores)
query = 
        SELECT
          cli.primeiro_nome AS primeiro_nome_cliente,
          cli.ultimo_nome AS ultimo_nome_cliente,
          cli.tipo_cliente,
          cli.data_nascimento AS data_nasc_cliente,
          cli.endereco AS endereco_cliente,
          cli.data_inclusao AS data_inclusao_cliente,
          cnt.num_conta,
          cnt.cod_cliente,
          cnt.cod_agencia,
          cnt.cod_colaborador AS cod_colaborador_da_conta,
          cnt.tipo_conta,
          cnt.data_abertura AS data_abertura_conta,
          cnt.saldo_total,
          cnt.saldo_disponivel,
          cnt.data_ultimo_lancamento,
          tr.cod_transacao,
          tr.data_transacao,
          tr.nome_transacao,
          tr.valor_transacao,
          prop.cod_proposta,
          prop.data_entrada_proposta AS data_entrada_prop,
          prop.taxa_juros_mensal AS taxa_juros_mensaL_prop,
          prop.valor_proposta AS valor_prop,
          prop.valor_financiamento AS valor_financiamento_prop,
          prop.valor_entrada AS valor_entrada_prop,
          prop.valor_prestacao AS valor_prestacao_prop,
          prop.quantidade_parcelas AS qtde_parcelas_prop,
          prop.carencia AS carencia_prop,
          prop.status_proposta AS status_prop,
          ag.nome AS nome_agencia,
          ag.endereco AS endereco_agencia,
          ag.cidade AS cidade_agencia,
          ag.uf AS uf_agencia,
          ag.data_abertura AS data_abentura_agencia,
          ag.tipo_agencia,
          colbag.cod_colaborador,
          colb.primeiro_nome AS primeiro_nome_colaborador,
          colb.ultimo_nome AS ultimo_nome_colaborador,
          colb.data_nascimento AS data_nasc_colaborador,
          colb.endereco AS endereco_colaborador
        FROM contas cnt LEFT JOIN clientes cli ON (cnt.cod_cliente = cli.cod_cliente)
        LEFT JOIN transacoes tr ON (cnt.num_conta = tr.num_conta)
        LEFT JOIN propostas_credito prop ON (cnt.cod_cliente = prop.cod_cliente)
        LEFT JOIN agencias ag ON (cnt.cod_agencia = ag.cod_agencia)
        LEFT JOIN colaborador_agencia colbag ON (cnt.cod_agencia = colbag.cod_agencia)
        LEFT JOIN colaboradores colb ON (colbag.cod_colaborador = colb.cod_colaborador)
        

# 1.5 Transformação da Junção das tabelas do Data Warehouse em um Dataframe
df_geral = pd.read_sql_query(query, conn )

# 1.6  Cópia do dataframe original para manipulação da cópia
df1 = df_geral.copy()

# 2. Análise Exploratória dos Dados

# 2.1 Demonstração das informações constantes no dataframe
# Legenda: número colunas, número de linhas, nome colunas, total de células com valores não nulos (non-null) por coluna
# e tipo de dado (legenda: object = texto; Int64 = inteiro; float64 = decilmal; dbdate = data;  datetime64[us, UTC] = data com horas, horas e minutos)
df1.info()

# 2.2 Identificação do número células em branco em cada coluna
df1.isna().sum()

# 2.3 Demonstração dos dados estatísticos das variáveis numéricas do dataframe

# 2.3.1 Tabela resumo com dados estatísticos das variáveis numéricas
#lista das colunas que foram desconsideradas nessa etapa: num_conta,	cod_cliente,	cod_agencia,	cod_colaborador_da_conta, cod_transacao, cod_proposta e cod_colaborador
colunas = ['saldo_total', 'saldo_disponivel', 'valor_transacao', 'taxa_juros_mensaL_prop', 'valor_prop','valor_financiamento_prop', 'valor_entrada_prop', 'valor_prestacao_prop', 'qtde_parcelas_prop', 'carencia_prop']
df2 = pd.DataFrame(df1, columns = colunas)
df2.describe()

# 2.3.2 Gráfico boxplot do saldo total nas contas bancárias para analisar distribuição dos valores
print('A média do saldo total nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_total'].mean()))
print('O desvio padrão do saldo total nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_total'].std()))
print('A mediana do saldo total nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_total'].median()))
print('O valor máximo de saldo total nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_total'].max()))
print('O valor mínimo de saldo total nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_total'].min()))
plt.rcParams["figure.figsize"] = [6.00, 4.00]
plt.rcParams["figure.autolayout"] = True
sns.boxplot(data = df1, y = df1['saldo_total'])
plt.show()
# Para identificar melhor os valores de saldo total acima de R$400 mil
colunas = ['nome_cliente', 'saldo_total']
df2 = pd.DataFrame(df1, columns = colunas)
df2[df2['saldo_total'] > 400000]

# 2.3.3 Gráfico boxplot do saldo disponível nas contas bancárias para analisar distribuição dos valores
print('A média do saldo disponível nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_disponivel'].mean()))
print('O desvio padrão do saldo disponível nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_disponivel'].std()))
print('A mediana do saldo disponível nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_disponivel'].median()))
print('O valor máximo de saldo disponível nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_disponivel'].max()))
print('O valor mínimo de saldo disponível nas contas bancárias é: {:.2f}'.format(df1.loc[:,'saldo_disponivel'].min()))
plt.rcParams["figure.figsize"] = [6.00, 4.00]
plt.rcParams["figure.autolayout"] = True
sns.boxplot(data = df1, y = df1['saldo_disponivel'])
plt.show()
# Para identificar melhor os valores de saldo disponível acima de R$400 mil
colunas = ['nome_cliente', 'saldo_disponivel']
df2 = pd.DataFrame(df1, columns = colunas)
df2[df2['saldo_disponivel'] > 400000]

# 2.3.4 Gráfico boxplot do valor das transações para analisar distribuição dos valores
print('A média do valor das transações é: {:.2f}'.format(df1.loc[:,'valor_transacao'].mean()))
print('O desvio padrão do valor das transações é: {:.2f}'.format(df1.loc[:,'valor_transacao'].std()))
print('A mediana do valor das transações é: {:.2f}'.format(df1.loc[:,'valor_transacao'].median()))
print('O valor máximo do valor das transações é: {:.2f}'.format(df1.loc[:,'valor_transacao'].max()))
print('O valor mínimo do valor das transações é: {:.2f}'.format(df1.loc[:,'valor_transacao'].min()))
plt.rcParams["figure.figsize"] = [6.00, 4.00]
plt.rcParams["figure.autolayout"] = True
sns.boxplot(data = df1, y = df1['valor_transacao'])
plt.show()

# 2.3.5 Gráfico boxplot do valor das propostas financeiras para analisar distribuição dos valores
print('A média do valor das propostas financeiras é: {:.2f}'.format(df1.loc[:,'valor_prop'].mean()))
print('O desvio padrão do valor das propostas financeiras é: {:.2f}'.format(df1.loc[:,'valor_prop'].std()))
print('A mediana do valor das propostas financeiras é: {:.2f}'.format(df1.loc[:,'valor_prop'].median()))
print('O valor máximo do valor das propostas financeiras é: {:.2f}'.format(df1.loc[:,'valor_prop'].max()))
print('O valor mínimo do valor das propostas financeiras é: {:.2f}'.format(df1.loc[:,'valor_prop'].min()))
plt.rcParams["figure.figsize"] = [6.00, 4.00]
plt.rcParams["figure.autolayout"] = True
sns.boxplot(data = df1, y = df1['valor_prop'])
plt.show()

# 2.4 Demonstração do total de valores distintos existentes em cada coluna
for i in df1.columns[0:39].tolist():
	print(i, ':', len(df1[i].astype(str).value_counts()))

# 2.5 Demonstração dos totais de valores das variáveis categóricas

# 2.5.1 Checagem dos tipos de contas bancárias e seus totais
df1.groupby(['tipo_conta']).size()

# 2.5.2 Checagem dos tipos de clientes e seus totais
df1.groupby(['tipo_cliente']).size()

# 2.5.3 Checagem dos nomes de transações e seus totais
df1.groupby(['nome_transacao']).size()

# 2.5.4 Checagem dos status da proposta de financiamento e seus totais
df1.groupby(['status_prop']).size()

# 2.5.5 Checagem dos nomes das agências bancárias e seus totais
df1.groupby(['nome_agencia']).size()

# 2.5.6 Checagem das cidades das agências bancárias e seus totais
df1.groupby(['cidade_agencia']).size()

# 2.5.7 Checagem dos estados das agências bancárias e seus totais
df1.groupby(['uf_agencia']).size()

# 2.5.8 Checagem dos tipos de agências bancárias e seus totais
df1.groupby(['tipo_agencia']).size()

# 2.5.9 Checagem da data mais recente de inclusão dos clientes
df1['data_inclusao_cliente'].min()

# 2.5.10 Checagem da data mais antiga de inclusão dos clientes
df1['data_inclusao_cliente'].max()

# 2.5.11 Checagem da data mais recente de inclusão dos clientes
df1['data_abentura_agencia'].min()

# 2.5.12 Checagem da data mais antiga de inclusão dos clientes
df1['data_abentura_agencia'].max()

# 3. Tratamento dos dados com Python
# exclusão colunas repetidas (com chaves estrangeiras);
# exclusão de dados sensíveis (cpf, cnpj, email e cep);
# renomear colunas (que tem título repetido entre as tabelas);
# concatenar colunas de primeiro e último nome para clientes e colaboradores.

# 3.1  Cópia do dataframe original para manipulação da cópia
# Cópia do dataframe para tratamento
df2 = df1.copy()

# 3.2 Junção do primeiro com o segundo nome dos clientes
df2['nome_cliente'] = df2['primeiro_nome_cliente'] + ' ' + df2['ultimo_nome_cliente']

# 3.3 Junção do primeiro com o segundo nome dos colaboradores
df2['nome_colaborador'] = df2['primeiro_nome_colaborador'] + ' ' + df2['ultimo_nome_colaborador']

# 3.4 Tratamento dos valores nulos
# Preenchimento das informações de clientes faltantes
df2['primeiro_nome_cliente'] = df2['primeiro_nome_cliente'].fillna(df2['primeiro_nome_cliente'].replace([None], 'Desconhecido'))
df2['ultimo_nome_cliente'] = df2['ultimo_nome_cliente'].fillna(df2['ultimo_nome_cliente'].replace([None], 'Desconhecido'))
df2['nome_cliente'] = df2['nome_cliente'].fillna(df2['nome_cliente'].replace([None], 'Desconhecido'))
df2['tipo_cliente'] = df2['tipo_cliente'].fillna(df2['tipo_cliente'].replace([None], 'Desconhecido'))
df2['data_nasc_cliente'] = df2['data_nasc_cliente'].fillna(df2['data_nasc_cliente'].median())
df2['endereco_cliente'] = df2['endereco_cliente'].fillna(df2['endereco_cliente'].replace([None], 'Desconhecido'))
df2['data_inclusao_cliente'] = df2['data_inclusao_cliente'].fillna(df2['data_inclusao_cliente'].median())
# Preenchimento das informações de propostas financeiras faltantes
df2['cod_proposta'] = df2['cod_proposta'].fillna(df2['cod_proposta'].replace([None], 0000))
df2['data_entrada_prop'] = df2['data_entrada_prop'].fillna(df2['data_entrada_prop'].median())
df2['taxa_juros_mensaL_prop'] = df2['taxa_juros_mensaL_prop'].fillna(df2['taxa_juros_mensaL_prop'].median())
df2['valor_prop'] = df2['valor_prop'].fillna(df2['valor_prop'].median())
df2['valor_financiamento_prop'] = df2['valor_financiamento_prop'].fillna(df2['valor_financiamento_prop'].median())
df2['valor_entrada_prop'] = df2['valor_entrada_prop'].fillna(df2['valor_entrada_prop'].median())
df2['valor_prestacao_prop'] = df2['valor_prestacao_prop'].fillna(df2['valor_prestacao_prop'].median())
df2['qtde_parcelas_prop'] = df2['qtde_parcelas_prop'].fillna(df2['qtde_parcelas_prop'].median())
df2['carencia_prop'] = df2['carencia_prop'].fillna(df2['carencia_prop'].median())
df2['status_prop'] = df2['status_prop'].fillna(df2['status_prop'].replace([None], 'Desconhecido'))
# Checagem se ainda existem valores nulos no novo dataframe
df2.isna().sum()

# 3.5 Engenharia de atributos
Geração de dim_dates e extração do uf da coluna endereço.

# 3.5.1 Classificação dos clientes em range de tempo de fidelidade ao banco
# Transfomação das datas para ano
df2['data_inclusao_cliente'] = pd.to_datetime(df2['data_inclusao_cliente'])
df2['ano_inclusao_cliente'] = pd.DatetimeIndex(df2['data_inclusao_cliente']).year
# Definição do tempo de fidelidade dos clientes
df2 ['tempo_fidelidade'] = 2024 - df2['ano_inclusao_cliente']
print('O valor máximo de fidelidade dos clientes é: {:.2f}'.format(df2.loc[:,'tempo_fidelidade'].max()))
print('O valor mínimo de fidelidade dos clientes é: {:.2f}'.format(df2.loc[:,'tempo_fidelidade'].min()))
# Criando um campo período com uma faixa de tempo de fidelidade dos clientes
print('Legenda: Recente (>=2018, ou seja, de 3 a  6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
bins = [-1, 6, 10, 14]
labels = ['Recente', 'Intermediário', 'Antigo']
df2['range_tempo_fidelidade'] = pd.cut(df2['tempo_fidelidade'], bins=bins, labels=labels)
pd.value_counts(df2.range_tempo_fidelidade)

# 3.5.2 Classificação dos clientes em range idade
# Transfomação das datas para ano
df2['data_nasc_cliente'] = pd.to_datetime(df2['data_nasc_cliente'])
df2['ano_nasc_cliente'] = pd.DatetimeIndex(df2['data_nasc_cliente']).year
# Definição da idade dos clientes
df2 ['idade_cliente'] = 2024 - df2['ano_nasc_cliente']
print('O valor máximo de idade dos clientes é: {:.2f}'.format(df2.loc[:,'idade_cliente'].max()))
print('O valor mínimo de idade dos clientes é: {:.2f}'.format(df2.loc[:,'idade_cliente'].min()))
# Criando um campo período com uma faixa de idade
print('Legenda: Jovem (Até 25 anos), Adulto (de 26 a 59 anos) e Melhor Idade (de 60 a 90 anos)')
bins = [-1, 25, 59, 90]
labels = ['Jovem', 'Adulto', 'Melhor Idade']
df2['range_idade_cliente'] = pd.cut(df2['idade_cliente'], bins=bins, labels=labels)
pd.value_counts(df2.range_idade_cliente)

# 3.5.3 Classificação dos colaboradores em range idade
# Transfomação das datas para ano
df2['data_nasc_colaborador'] = pd.to_datetime(df2['data_nasc_colaborador'])
df2['ano_nasc_colaborador'] = pd.DatetimeIndex(df2['data_nasc_colaborador']).year
# Definição da idade dos colaboradores
df2 ['idade_colaborador'] = 2024 - df2['ano_nasc_colaborador']
print('O valor máximo de idade dos colaboradores é: {:.2f}'.format(df2.loc[:,'idade_colaborador'].max()))
print('O valor mínimo de idade dos colaboradores é: {:.2f}'.format(df2.loc[:,'idade_colaborador'].min()))
# Criando um campo período com uma faixa de idade
print('Legenda: Jovem (Até 25 anos), Adulto (de 26 a 59 anos) e Melhor Idade (de 60 a 90 anos)')
bins = [-1, 25, 59, 90]
labels = ['Jovem', 'Adulto', 'Melhor Idade']
df2['range_idade_colaborador'] = pd.cut(df2['idade_colaborador'], bins=bins, labels=labels)
pd.value_counts(df2.range_idade_colaborador)

# 3.5.4 Classificação das agências em range de tempo de funcionamento
# Transfomação das datas para ano
df2['data_abentura_agencia'] = pd.to_datetime(df2['data_abentura_agencia'])
df2['ano_abentura_agencia'] = pd.DatetimeIndex(df2['data_abentura_agencia']).year
# Definição da idade das agências
df2 ['idade_agencia'] = 2024 - df2['ano_abentura_agencia']
print('O valor máximo de idade das agências é: {:.2f}'.format(df2.loc[:,'idade_agencia'].max()))
print('O valor mínimo de idade das agências é: {:.2f}'.format(df2.loc[:,'idade_agencia'].min()))
# Criando um campo período com uma faixa de idade das agências
print('Legenda: Recente (>=2018, ou seja, de 3 a 6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
bins = [-1, 6, 10, 14]
labels = ['Recente', 'Intermediário', 'Antigo']
df2['range_idade_agencia'] = pd.cut(df2['idade_agencia'], bins=bins, labels=labels)
pd.value_counts(df2.range_idade_agencia)

# 3.2.5 Classificação das contas em range de tempo de atividade
# Transfomação das datas para ano
df2['data_abertura_conta'] = pd.to_datetime(df2['data_abertura_conta'])
df2['ano_abentura_conta'] = pd.DatetimeIndex(df2['data_abertura_conta']).year
# Definição do tempo de atividade das contas
df2 ['idade_conta'] = 2024 - df2['ano_abentura_conta']
print('O valor máximo de idade das contas é: {:.2f}'.format(df2.loc[:,'idade_conta'].max()))
print('O valor mínimo de idade das contas é: {:.2f}'.format(df2.loc[:,'idade_conta'].min()))
# Criando um campo período com uma faixa de idade das contas
print('Legenda: Recente (>=2018, ou seja, de 3 a 6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
bins = [-1, 6, 10, 14]
labels = ['Recente', 'Intermediário', 'Antigo']
df2['range_idade_conta'] = pd.cut(df2['idade_conta'], bins=bins, labels=labels)
pd.value_counts(df2.range_idade_conta)

# 3.5.6 Classificação dos lançamentos em range de tempo do último realizado  (tempo de inatividade)
# Transfomação das datas para ano
df2['data_ultimo_lancamento'] = pd.to_datetime(df2['data_ultimo_lancamento'])
df2['ano_ultimo_lancamento'] = pd.DatetimeIndex(df2['data_ultimo_lancamento']).year
# Definição da idade dos ultimos lançamentos
df2 ['idade_ultimo_lancamento'] = 2024 - df2['ano_ultimo_lancamento']
print('O valor máximo de idade dos últimos lançamentos é: {:.2f}'.format(df2.loc[:,'idade_ultimo_lancamento'].max()))
print('O valor mínimo de idade das últimos lançamentos é: {:.2f}'.format(df2.loc[:,'idade_ultimo_lancamento'].min()))
# Criando um campo período com uma faixa de idade dos últimos lançamentos
print('Legenda: Recente (>=2018, ou seja, de 3 a 6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
bins = [-1, 6, 10, 14]
labels = ['Recente', 'Intermediário', 'Antigo']
df2['range_ultimo_lancamento'] = pd.cut(df2['idade_ultimo_lancamento'], bins=bins, labels=labels)
pd.value_counts(df2.range_ultimo_lancamento)

# 3.5.7 Classificação do tempo da entrega das propostas financeiras em ANOS
# Transfomação das datas para ano
df2['data_entrada_prop'] = pd.to_datetime(df2['data_entrada_prop'])
df2['ano_entrada_prop'] = pd.DatetimeIndex(df2['data_entrada_prop']).year
# Definição do tempo em anos da entrega das propostas financeiras
df2 ['total_anos_entrada_prop'] = 2024 - df2['ano_entrada_prop']
print('O valor máximo de anos de entrega das propostas financeiras é: {:.2f}'.format(df2.loc[:,'total_anos_entrada_prop'].max()))
print('O valor mínimo de anos de entrega das propostas financeiras é: {:.2f}'.format(df2.loc[:,'total_anos_entrada_prop'].min()))
# Criando um campo período de tempo em anos da entrega das propostas financeiras
print('Legenda: Recente (>=2018, ou seja, de 3 a 6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
bins = [-1, 6, 10, 14]
labels = ['Recente', 'Intermediário', 'Antigo']
df2['range_tempo_entrada_prop'] = pd.cut(df2['total_anos_entrada_prop'], bins=bins, labels=labels)
pd.value_counts(df2.range_tempo_entrada_prop)

# 3.5.8 Classificação do tempo da entrega das propostas financeiras em MESES
# Transfomação das datas para mês
df2['data_entrada_prop'] = pd.to_datetime(df2['data_entrada_prop'])
df2['mes_entrada_prop'] = pd.DatetimeIndex(df2['data_entrada_prop']).month
# Definição do tempo da entrega das propostas financeiras
print('O valor máximo de meses de entrega das propostas financeiras é: {:.2f}'.format(df2.loc[:,'mes_entrada_prop'].max()))
print('O valor mínimo de meses de entrega das propostas financeiras é: {:.2f}'.format(df2.loc[:,'mes_entrada_prop'].min()))
# Criando um campo período de tempo em meses da entrega das propostas financeiras
print('Legenda: Primeiro Trimestre (Janeiro a Março), Segundo Trimestre (Abril a Junho), Terceiro Trimestre (Julho a Setembro) e Quarto Trimestre (Outubro a Dezembro)')
bins = [-1, 3, 4, 8, 12]
labels = ['Primeiro Trimestre', 'Segundo Trimestre', 'Terceiro Trimestre', 'Quarto Trimestre']
df2['range_mes_entrada_prop'] = pd.cut(df2['mes_entrada_prop'], bins=bins, labels=labels)
pd.value_counts(df2.range_mes_entrada_prop)

# 3.5.9 Classificação do tempo da entrega das propostas financeiras em DIAS
# Transfomação das datas para dia
df2['data_entrada_prop'] = pd.to_datetime(df2['data_entrada_prop'])
df2['dia_entrada_prop'] = pd.DatetimeIndex(df2['data_entrada_prop']).day
# Definição do tempo da entrega das propostas financeiras
print('O valor máximo de dias de entrega das propostas financeiras é: {:.2f}'.format(df2.loc[:,'dia_entrada_prop'].max()))
print('O valor mínimo de dias de entrega das propostas financeiras é: {:.2f}'.format(df2.loc[:,'dia_entrada_prop'].min()))
# Criando um campo período de tempo em dias da entrega das propostas financeiras
print('Legenda: Primeira Quinzena (dia 01 a 15) e Segunda Quinzena (dia 16 a 31)')
bins = [-1, 15, 31]
labels = ['Primeira Quinzena', 'Segunda Quinzena']
df2['range_dia_entrada_prop'] = pd.cut(df2['dia_entrada_prop'], bins=bins, labels=labels)
pd.value_counts(df2.range_dia_entrada_prop)

# 3.5.10 Classificação do tempo da entrega das propostas financeiras em DIAS DA SEMANA
# Formatando o campo data
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
# Transfomação das datas para dia da semana
print('Legenda: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday')
df2['data_entrada_prop'] = pd.to_datetime(df2['data_entrada_prop'])
df2['dia_semana_entrada_prop'] = pd.DatetimeIndex(df2['data_entrada_prop']).day_name(locale = 'en_US.utf8')

# 3.5.11 Classificação do tempo das transações em ANOS
# Transfomação das datas para ano
df2['data_transacao'] = pd.to_datetime(df2['data_transacao'])
df2['ano_transacao'] = pd.DatetimeIndex(df2['data_transacao']).year
# Definição do tempo em anos das transações
df2 ['total_anos_transacao'] = 2024 - df2['ano_transacao']
print('O valor máximo de anos das transações é: {:.2f}'.format(df2.loc[:,'total_anos_transacao'].max()))
print('O valor mínimo de anos das transações é: {:.2f}'.format(df2.loc[:,'total_anos_transacao'].min()))
# Criando um campo período de tempo em anos das transações
print('Legenda: Recente (>=2018, ou seja, de 3 a 6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
bins = [-1, 6, 10, 14]
labels = ['Recente', 'Intermediário', 'Antigo']
df2['range_total_anos_transacao'] = pd.cut(df2['total_anos_transacao'], bins=bins, labels=labels)
pd.value_counts(df2.range_total_anos_transacao)

# 3.5.12 Classificação do tempo das transações em MESES
# Transfomação das datas para mês
df2['data_transacao'] = pd.to_datetime(df2['data_transacao'])
df2['mes_transacao'] = pd.DatetimeIndex(df2['data_transacao']).month
# Definição do tempo das transações
print('O valor máximo de meses das transações é: {:.2f}'.format(df2.loc[:,'mes_transacao'].max()))
print('O valor mínimo de meses das transações é: {:.2f}'.format(df2.loc[:,'mes_transacao'].min()))
# Criando um campo período de tempo em meses das transações
print('Legenda: Primeiro Trimestre (Janeiro a Março), Segundo Trimestre (Abril a Junho), Terceiro Trimestre (Julho a Setembro) e Quarto Trimestre (Outubro a Dezembro)')
bins = [-1, 3, 4, 8, 12]
labels = ['Primeiro Trimestre', 'Segundo Trimestre', 'Terceiro Trimestre', 'Quarto Trimestre']
df2['range_mes_transacao'] = pd.cut(df2['mes_transacao'], bins=bins, labels=labels)
pd.value_counts(df2.range_mes_transacao)

# 3.5.13 Classificação do tempo das transações em DIAS
# Transfomação das datas para dia
df2['data_transacao'] = pd.to_datetime(df2['data_transacao'])
df2['dia_transacao'] = pd.DatetimeIndex(df2['data_transacao']).day
# Definição do tempo das transações
print('O valor máximo de dias das transações é: {:.2f}'.format(df2.loc[:,'dia_transacao'].max()))
print('O valor mínimo de dias das transações é: {:.2f}'.format(df2.loc[:,'dia_transacao'].min()))
# Criando um campo período de tempo em dias das transações
print('Legenda: Primeira Quinzena (dia 01 a 15) e Segunda Quinzena (dia 16 a 31)')
bins = [-1, 15, 31]
labels = ['Primeira Quinzena', 'Segunda Quinzena']
df2['range_dia_transacao'] = pd.cut(df2['dia_transacao'], bins=bins, labels=labels)
pd.value_counts(df2.range_dia_transacao)

# 3.5.14 Classificação do tempo das transações em DIAS DA SEMANA
# Formatando o campo data
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
# Transfomação das datas para dia da semana
print('Legenda: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday')
df2['data_transacao'] = pd.to_datetime(df2['data_transacao'])
df2['dia_semana_transacao'] = pd.DatetimeIndex(df2['data_transacao']).day_name(locale = 'en_US.utf8')

# 3.5.15 Classificação do tempo das transações em HORÁRIOS DO DIA
# Criando um campo hora e minuto
df2['hora_transacao'] = df2['data_transacao'].dt.strftime('%H')
df2['hora_transacao'] = df2['hora_transacao'].astype(int)
# Criando um campo período com uma faixa de acordo com as horas
print('Legenda: Madrugada (de 0 a 6h), Manhã (de 7 a 12h), Tarde (13 a 18h) e Noite (19 a 24h)')
bins = [-1, 6, 12, 18, 24]
labels = ['Madrugada', 'Manhã', 'Tarde', 'Noite']
df2['periodo_transacao'] = pd.cut(df2['hora_transacao'], bins=bins, labels=labels)
pd.value_counts(df2.periodo_transacao)

# 3.5.16 Extração da sigla do endereço dos clientes
df2['uf_cliente'] = df2['endereco_cliente'].str[-2:]

# 3.5.17 Extração da sigla do endereço dos colaboradores
df2['uf_colaborador'] = df2['endereco_colaborador'].str[-2:]

# 4. Respondendo às Perguntas de Negócio usando Python

# Cópia do dataframe para tratamento
df3 = df2.copy()

### 4.1 Indicador: Lucro do Banco

# 4.1.1 Pergunta 1: Em relação as transações bancárias, o banco enviou ou recebeu mais dinheiro ao longo do tempo?
# Definição do máximo e mínimo dos valores das transações
print('O valor máximo das transações é: {:.2f}'.format(df2.loc[:,'valor_transacao'].max()))
print('O valor mínimo das transações é: {:.2f}'.format(df2.loc[:,'valor_transacao'].min()))
# Criando um campo marcação se é entrada ou saída
print('Legenda:' )
print('Entrada (são valores positivos = DOC - Recebido, TED - Recebido, Pix - Recebido e Depósito em espécie')
print('Saída (Compra Crédito, Compra Débito, DOC - Realizado, TED - Realizado, Saque, Pix Saque, Pix - Realizado, Pagamento de boleto, Transferência entre CC - Crédito e Transferência entre CC - Débito')
bins = [-132101, 0, 480271]
labels = ['Saída', 'Entrada']
df3['tipo_transacao'] = pd.cut(df3['valor_transacao'], bins=bins, labels=labels)
pd.value_counts(df3.tipo_transacao)
#Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['tipo_transacao', 'valor_transacao']
colunas_groupby = ['tipo_transacao']
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index()
data_plot
# seleção das colunas de interesse
colunas = ['tipo_transacao', 'valor_transacao']
# seleção das colunas pelas quais será realizada a segmentação
colunas_groupby = ['tipo_transacao']
# seleção de linhas e colunas, agrupar e aplicar a operação de máxima, Eu utilizo o resert_index ao final para ele transformar o index em uma nova coluna para que se possa fazer um gráfico
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index()
# Desenho do gráfico de barras verticais
px.bar(data_plot, x='tipo_transacao', y='valor_transacao')

# 4.1.2 Pergunta 2: Pergunta 2 - Como está o valor das transações financeiras do banco ao longo do tempo?
sns.set_palette('colorblind')
sns.relplot(x='tempo_fidelidade', y='valor_transacao', hue='range_tempo_fidelidade', col='range_idade_cliente', data=df3)
#Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
print('Legenda idade dos clientes: Jovem (Até 25 anos), Adulto (de 26 a 59 anos) e Melhor Idade (de 60 a 90 anos)')
print('Legenda dos períodos analisados: Recente (>=2018, ou seja, de 3 a 6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
colunas = ['range_idade_cliente', 'range_tempo_fidelidade', 'valor_transacao']
colunas_groupby = ['range_idade_cliente', 'range_tempo_fidelidade']
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index()
data_plot

# 4.1.3 Pergunta 3: Qual o valor das propostas financeiras ao longo do tempo?
#Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
perg3 = sns.boxplot(x='range_idade_cliente', y='valor_prop', hue = 'range_tempo_fidelidade', data=df3)
#Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
print('Legenda idade dos clientes: Jovem (Até 25 anos), Adulto (de 26 a 59 anos) e Melhor Idade (de 60 a 90 anos)')
print('Legenda dos períodos analisados: Recente (>=2018, ou seja, de 3 a 6 anos), Intermediário (>2013 e <= 2017, ou seja, de 7 a 10 anos) e Antigo (<=2013, ou seja, de 11 a 14 anos)')
colunas = ['range_idade_cliente', 'range_tempo_fidelidade', 'valor_prop']
colunas_groupby = ['range_idade_cliente', 'range_tempo_fidelidade']
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index()
data_plot

# 4.1.4 Pergunta 4: Lucro (de Montante de juros recebidos) com empréstimos está maior ao longo do tempo?
# Lucro do banco por proposta financeira = (número de parcelas * valor da parcela) – valor_proposta
df3['lucro_prop'] = (df3['qtde_parcelas_prop'] * df3['valor_prestacao_prop']) - df3['valor_prop']
# seleção das colunas
colunas = ['range_tempo_fidelidade', 'lucro_prop']
# seleção das colunas pelas quais será realizada a segmentação
colunas_groupby = ['range_tempo_fidelidade']
# seleção de linhas e colunas, agrupar e aplicar a operação de máxima
# eu utilizo o resert_index ao final para ele transformação o index em uma nova coluna para que se possa fazer um gráfico
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).max().reset_index()
# desenho do histograma
px.bar(data_plot, y='lucro_prop', x='range_tempo_fidelidade')

### 4.2 Indicador: Perfil dos Clientes

# 4.2.1 Pergunta 5: Como é a distribuição da idade dos clientes por agência?
sns.set_palette('colorblind')
sns.relplot(x='idade_cliente', y='nome_agencia', hue='range_idade_cliente', data=df3)

# 4.2.2 Pergunta 6: Como é a distribuição da idade dos clientes por tempo de vínculo com o banco?
sns.set_palette('colorblind')
sns.relplot(x='range_tempo_fidelidade', y='idade_cliente', hue='range_idade_cliente', data=df3)

# 4.2.3 Pergunta 7: O perfil dos clientes em relação ao tipo de transações mudou ao longo do tempo?
sns.set_palette('colorblind')
sns.relplot(x='saldo_disponivel', y='nome_transacao', hue='range_tempo_fidelidade', col='range_idade_cliente', data=df3)
sns.set_palette('colorblind')
sns.relplot(x='saldo_disponivel', y='uf_cliente', hue='range_tempo_fidelidade', data=df3)

# 4.2.4 Pergunta 8: O perfil dos clientes em relação a movimentações bancárias (saldo na conta/ valor de empréstimo) mudou ao longo do tempo?
# movimentações bancárias (saldo na conta/ valor de empréstimo)
df3['moviment_banc'] = df3['saldo_disponivel'] + df3['lucro_prop']
#Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['saldo_disponivel', 'lucro_prop', 'moviment_banc']
colunas_groupby = ['moviment_banc']
tab = df3.loc[:,colunas]
tab
sns.set_palette('colorblind')
sns.relplot(x='moviment_banc', y='tipo_transacao', hue='range_tempo_fidelidade', col='range_idade_cliente', data=df3)

### 4.3 Indicador: Situação das Contas Bancárias

# 4.3.1 Pergunta 9: Como está a inatividade das contas bancárias ao longo do tempo?
# Criação do gráfico de barras
sns.barplot(x='idade_ultimo_lancamento', y='uf_cliente', hue='range_idade_cliente', data=df3, palette='viridis')
# Adicionar título e rótulos
plt.title('Gráfico de Barras sobre Inatividade dos Clientes')
plt.xlabel('Tempo de Inatividade (anos)')
plt.ylabel('Localidade dos clientes')
# Mostrar o gráfico
plt.show()

# 4.3.2 Pergunta 10: O saldo das contas tem ligação o tipo de agência (física ou digital)?
# Obs: Avaliar a popularidade da agência digital em comparação com a agência física.
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['tipo_agencia', 'cod_cliente']
colunas_groupby = ['tipo_agencia']
# contagem do volume de transação
print('Volume de clientes por tipo de agência')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_cliente', ascending=False)
data_plot
# Criação do gráfico de barras
sns.barplot(x='saldo_disponivel', y='tipo_agencia', data=df3, palette='viridis')
# Adicionar título e rótulos
plt.xlabel('Saldo Disponível na conta (R$)')
plt.ylabel('Tipo de agência')
# Mostrar o gráfico
plt.show()

# 4.3.3 Pergunta 11: O saldo das contas tem ligação com a localidade?
# Criação do gráfico de barras
sns.barplot(x='saldo_disponivel', y='uf_agencia', data=df3, palette='viridis')
# Adicionar título e rótulos
plt.xlabel('Saldo Disponível na conta (R$)')
plt.ylabel('Estado da agência')
# Mostrar o gráfico
plt.show()

### 4.4 Indicador: Status das Transações Financeiras

# 4.4.1 Pergunta 12: Qual dia da semana tem, em média, maior volume de transações e qual tem, também em média, maior valor movimentado?
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['dia_semana_transacao', 'valor_transacao']
colunas_groupby = ['dia_semana_transacao']
# soma do valor da transação
print('Valores movimentados com transações por dia da semana')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index().sort_values(by='valor_transacao', ascending=False)
data_plot
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['dia_semana_transacao', 'cod_transacao']
colunas_groupby = ['dia_semana_transacao']
# contagem do volume de transação
print('Volume de transações por dia da semana')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_transacao', ascending=False)
data_plot

# 4.4.2 Pergunta 13: O BanVic tem, em média, os maiores valores movimentados no início ou final de mês? (Considere início do mês como sendo os primeiro 15 dias e o final do mês sendo os últimos 15 dias de cada mês).
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['range_dia_transacao', 'valor_transacao']
colunas_groupby = ['range_dia_transacao']
# soma do valor da transação
print('Valores movimentados com transações por quinzena do mês')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index().sort_values(by='valor_transacao', ascending=False)
data_plot
#Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['range_dia_transacao', 'cod_transacao']
colunas_groupby = ['range_dia_transacao']
# contagem do volume de transação
print('Volume de transações por quinzena do mês')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_transacao', ascending=False)
data_plot

# 4.4.3 Pergunta 14: O montante da transação tem relação com período do dia que é executada?
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['periodo_transacao', 'valor_transacao']
colunas_groupby = ['periodo_transacao']
# soma do valor da transação
print('Valores movimentados com transações por período do dia')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index().sort_values(by='valor_transacao', ascending=False)
data_plot

# 4.4.4 Pergunta 15: O tipo de transação tem relação ao mês do ano que é executada?
Explorar como o PIX afetou as transações.
print('Número de transações por mês')
tab_tran_mes = pd.crosstab(index=df3['nome_transacao'], columns=df3['mes_transacao'])
tab_tran_mes
print('Número de transações por mês')
tab_tran_mes.plot.bar(stacked=True)
plt.show()
#Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['nome_transacao', 'cod_transacao']
colunas_groupby = ['nome_transacao']
# contagem do volume de transação
print('Volume de transações por quinzena do mês')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_transacao', ascending=False)
data_plot

# 4.4.5 Pergunta 16: O tipo de transação mudou ao longo do tempo (anos)?
# Entender como o PIX afetou as transações: identificar padrões de inatividade.
print('Número de transações por ano')
tab_tran_ano = pd.crosstab(index=df3['nome_transacao'], columns=df3['ano_transacao'])
tab_tran_ano
print('Número de transações por ano')
tab_tran_ano.plot.bar(stacked=True)
plt.show()

### 4.5 Indicador: Status das Propostas de Crédito

# 4.5.1 Pergunta 17: Qual o tempo de vínculo com o banco dos clientes que pedem proposta financeira?
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['tempo_fidelidade', 'cod_proposta']
colunas_groupby = ['tempo_fidelidade']
# volume de propostas financeiras enviadas
print('Tempo de fidelidade dos clientes por volume de propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_proposta', ascending=False)
data_plot

# 4.5.2 Pergunta 18: Existe vínculo entre o período do ano do envio da proposta e os valores emprestados?
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['range_mes_entrada_prop', 'cod_proposta']
colunas_groupby = ['range_mes_entrada_prop']
# volume de propostas financeiras enviadas por mês do ano
print('Mês do ano por volume de propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_proposta', ascending=False)
data_plot
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['range_mes_entrada_prop', 'valor_prop']
colunas_groupby = ['range_mes_entrada_prop']
# valor das propostas financeiras enviadas por mês do ano
print('Mês do ano por valor das propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index().sort_values(by='valor_prop', ascending=False)
data_plot

# 4.5.3 Pergunta 19: Qual colaborador e agência têm mais propostas financeiras aprovadas? Em tramitação?
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['nome_colaborador', 'cod_proposta']
colunas_groupby = ['nome_colaborador']
# volume de propostas financeiras enviadas por colaborador
print('Colaborador por volume de propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_proposta', ascending=False)
data_plot
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['nome_colaborador', 'valor_prop']
colunas_groupby = ['nome_colaborador']
# valor das propostas financeiras enviadas por colaborador
print('Colaborador por valor das propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index().sort_values(by='valor_prop', ascending=False)
data_plot
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['nome_agencia', 'cod_proposta']
colunas_groupby = ['nome_agencia']
# volume de propostas financeiras enviadas por colaborador
print('Colaborador por volume de propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_proposta', ascending=False)
data_plot
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = ['nome_agencia', 'valor_prop']
colunas_groupby = ['nome_agencia']
# valor das propostas financeiras enviadas por agência
print('Agência por valor das propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).sum().reset_index().sort_values(by='valor_prop', ascending=False)
data_plot

# 4.5.4 Pergunta 20: Existe vínculo entre idade dos colaboradores e total de propostas financeiras recebidas?
# Seleção dos dados de interesse para gerar uma tabela resumo (data_plot)
colunas = [ 'idade_colaborador', 'cod_proposta']
colunas_groupby = ['idade_colaborador']
# volume de propostas financeiras enviadas por colaborador
print('Colaborador por volume de propostas financeiras enviadas')
data_plot = df3.loc[:,colunas].groupby(colunas_groupby).nunique().reset_index().sort_values(by='cod_proposta', ascending=False)
data_plot

# 5. Exportação do dataframe tratado .csv para ser inserido no Power BI

# 5.1 Limpeza do dataframe excluindo colunas criadas apenas para fazer cálculos
# Limpar a base das colunas intermediárias que eu criei apenas para fazer cálculos
df4 = df3[['tipo_cliente', 'data_inclusao_cliente', 'nome_cliente', 'idade_cliente','range_idade_cliente', 'uf_cliente', 'num_conta', 'range_tempo_fidelidade', 'cod_cliente', 'cod_agencia', 'cod_colaborador_da_conta', 'tipo_conta', 'data_abertura_conta', 'saldo_total', 'saldo_disponivel', 'data_ultimo_lancamento', 'range_idade_conta', 'range_ultimo_lancamento', 'cod_transacao', 'data_transacao', 'nome_transacao', 'valor_transacao', 'range_total_anos_transacao', 'range_mes_transacao', 'range_dia_transacao', 'dia_semana_transacao', 'hora_transacao', 'periodo_transacao', 'tipo_transacao', 'cod_proposta', 'data_entrada_prop', 'taxa_juros_mensaL_prop', 'valor_prop', 'valor_financiamento_prop', 'valor_entrada_prop', 'valor_prestacao_prop', 'qtde_parcelas_prop', 'carencia_prop', 'status_prop',  'range_tempo_entrada_prop', 'range_mes_entrada_prop', 'range_dia_entrada_prop', 'dia_semana_entrada_prop', 'lucro_prop',  'nome_agencia', 'endereco_agencia', 'cidade_agencia', 'uf_agencia', 'data_abentura_agencia', 'tipo_agencia', 'range_idade_agencia', 'moviment_banc', 'cod_colaborador',  'nome_colaborador', 'idade_colaborador', 'range_idade_colaborador', 'uf_colaborador']]

# 5.2 Exportação do dataframe para formato .csv
df4.to_csv('BancoVic_tab_TRATADAS.csv', index=False)
