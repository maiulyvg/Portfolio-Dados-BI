# **Projeto de Dados Financeiros com base em um Base de Dados de um Banco Fictício**

## Introdução
Focando em demostrar os diferenciais do Banco MG em relação as outras instituições financeiras do Brasil, foi realizado um projeto de Análise de Dados focando em ampliar a atuação do banco no mercado. 
Para a realização do projeto, o Banco disponibilizou 7 tabelas em formato .csv geradas pelo servidor da nuvem da empresa, onde estão os dados do Sistema de Gestão de Recursos Empresariais (ERP), o Sistema de Gerenciamento de Relacionamento com Clientes (CRM) e Controle de dados de Marketing (em plataforma própria). 

## Indicadores de Negócio
Como etapa prévia a Análise dos Dados, foi realizada a definição dos indicadores de negócio a partir  dos dados disponíveis. 
Posteriormente, foram definidas perguntas de negócio para analisar a situação atual do Banco MG, que foram separadas por indicador de negócio.

### 📍 Lucro do banco
- Pergunta 1 - Em relação as transações bancárias, o banco enviou ou recebeu mais dinheiro ao longo do tempo?  
- Pergunta 2 - Como está o valor das transações financeiras do banco ao longo do tempo?
- Pergunta 3 - Qual o valor das propostas financeiras ao longo do tempo? 
- Pergunta 4 - Montante de juros recebidos com empréstimos está maior ao longo do tempo? Ou seja, a taxa de juros das propostas financeiras (empréstimo) está beneficiando o banco?

### 📍 Perfil dos clientes
> Pergunta 5 - Como é a distribuição da idade por agência? 
> Pergunta 6 - Como é a distribuição da idade dos clientes por tempo de vínculo com o banco?
> Pergunta 7 - O perfil dos clientes em relação ao tipo de transações mudou ao longo do tempo? 
> Pergunta 8 - O perfil dos clientes em relação a movimentações bancárias (saldo na conta/ lucro de propostas de financiamento) mudou ao longo do tempo?
> 
### 📍 Situação das contas bancárias
> Pergunta 9 - Como está a inatividade das contas bancárias ao longo do tempo? 
> Pergunta 10 - O saldo das contas tem ligação o tipo de agência (física ou digital)?
> Pergunta 11 - O saldo das contas tem ligação com a localidade?

### 📍 Status das transações financeiras
> Pergunta 12 - Qual dia da semana tem, em média, maior volume de transações e qual tem, também em média, maior valor movimentado?
> Pergunta 13 - O BanVic tem, em média, os maiores valores movimentados no início ou final de mês? (Considere início do mês como sendo os primeiro 15 dias e o final do mês sendo os últimos 15 dias de cada mês).
> Pergunta 14 - O montante da transação tem relação com período do dia que é executada? 
> Pergunta 15 - O tipo de transação tem relação com o mês do ano que é executada?
> Pergunta 16 - O tipo de transação mudou ao longo dos anos?

### 📍 Status das propostas de crédito
> Pergunta 17 - Qual o tempo de vínculo com o banco dos clientes que pedem proposta financeira? 
> Pergunta 18 - Existe vínculo entre o período do ano do envio da proposta e os valores emprestados? 
> Pergunta 19 - Qual colaborador e agência têm mais propostas financeiras aprovadas? Em tramitação?
> Pergunta 20 - Existe vínculo entre idade dos colaboradores e total de propostas financeiras recebidas?


## Análise Realizadas
Primeiramente, foi feita a transferência de dados de EPR e CRM em csv para um Banco de Dados Relacional empregando SQLite3.
Na sequência foi realizada consulta do banco de dados utilizando SQL para consultas no banco de dados.
E dando início a análise de dados, foram escritos scripts com Python para análise exploratória, tratamento dos dados e resposta a perguntas de negócio. 
No arquivo analise_dados_financeiros.py, que consta nesse repositório, são descritas as análises que foram necessárias para o entendimento do negócio e que podem ser úteis no suporte para a tomada de decisão.
Assim como o Tratamento dos Dados, as Análises de Dados também foram realizadas com a linguagem Python e constam em detalhe no script.

## Vizualização de Dados:
Com base nos dados financeiros tratados foi gerado o dashboard em Power BI, que está disponível [aqui](https://app.powerbi.com/view?r=eyJrIjoiNjlhODNhYWYtZjQ1My00YmU0LWFiNGMtZTkzZDU0MjM5MzhhIiwidCI6IjdiMjlkMzdmLTA2NTQtNDE5OC05ODljLTVkMzYyN2RkZDQ3NCJ9)


## Resumo das Respostas das Perguntas de Negócio 
### 📍 Lucro do banco
> O Banco teve mais entradas R$ 8.280250e+08 (DOC - Recebido, TED - Recebido, Pix - Recebido e Depósito em espécie) do que saídas R$ -3.173538e+08 (Compra Crédito, Compra Débito, DOC - Realizado, TED - Realizado, Saque, Pix Saque, Pix - Realizado, Pagamento de boleto, Transferência entre CC - Crédito e Transferência entre CC – Débito). Demonstrando um balanço financeiro positivo da ordem de 2,5 vezes.
> Observa-se também que clientes adultos com 4 a 8 anos de vínculo com o banco têm o maior montante de valor de transações (da ordem de R$ 400mil) enquanto clientes jovens e da melhor idade com 4 a 8 anos de vínculo com o banco têm o segundo maior montante de valor de transações (variando da ordem de R$200 a 300mil). Podendo-se concluir que em média após 4 anos de vínculo com o Banco eles se sentem confiantes para fazer movimentações financeiras de grande ordem de valor.
> Por sua vez o valor das propostas de crédito varia em média entre R$120 a 250 mil, sendo geralmente solicitadas por clientes adultos e da melhor idade em todos os períodos de vínculo com o banco (recente, intermediário e antigo). Destaca-se que os clientes jovens de até 4 anos de vínculo com o banco também tem demonstrado interesse em realizar propostas de crédito. Por fim, destaca-se que o lucro com empréstimos está decrescendo ao longo do tempo de vínculo com o banco, sendo mais interessante incentivar os clientes com até quadro anos de vínculo a fazerem propostas de crédito.

### 📍 Perfil dos clientes
> As agências demonstram um comportamento homogêneo, com clientes em quase todas as faixas etárias (de 17 a 82 anos), com exceção da Agência de Recife é que tem um nicho de clientes menor e com idades que variam de 30 a 65 anos. Fato que pode ser explicado por essa agência ter sido a última a ser aberta pelo banco em 2021. 
> Em relação distribuição da idade dos clientes por tempo de vínculo com o banco, nota-se que os clientes adultos são maioria durante todo o período, seguido pelos clientes na melhor idade. Sendo que ambos têm uma distribuição homogênea em todo o período. Com exceção dos clientes jovens que tem menor contingente e se concentram em até 8 anos de vínculo com o banco.
> Constata-se que o perfil dos clientes mudou em relação ao tipo de transações mudou ao longo do tempo, clientes antigos realizaram menos transações e de valores mais baixos, enquanto clientes recentes realizaram mais transações e de valores mais altos. 
> Por outro lado, todos os perfis de clientes (jovem, adulto e melhor idade) apresentam transações em média da ordem R$200mil. Com exceção de alguns clientes adultos e da melhor idade que pontualmente fizeram transações da ordem de 300 a 400mil.

### 📍 Situação das contas bancárias
> Clientes na melhor idade demonstram as maiores taxas de inatividade das contas bancárias ao longo do tempo, enquanto clientes jovens e adultos demonstram taxas parecidas de movimentação.
> Embora o banco digital tenha iniciado suas atividades apenas em 2015, ele apresenta grande adesão por parte dos clientes. Visto que a agência digital tem 460 contas e apresenta um saldo disponível nas contas da ordem de 250 mil. Enquanto as nove agências físicas concentram 539 contas com saldo disponível nas contas da ordem de 280 mil. Demonstrando que em poucos anos a agência digital ganhou muito adeptos.
> Observa-se que o saldo das contas tem ligação com a localidade, todavia este oscila da ordem de nem R$100 mil entre o saldo médio disponíveis nas contas por estado. O estado com maior saldo é o Rio Grande do Sul (saldo de aproximadamente R$290 mil) e estado com menor saldo é Santa Catarina (saldo de aproximadamente R$230 mil).

### 📍 Status das transações financeiras
> O dia da semana tem, em média, com maior volume de transações e com maior valor movimentado é quinta-feira, com valores de R$ 1.426948e+08 e totalizando 21.120 transações.
> Enquanto a Segunda Quinzena tem, em média, com maior volume de transações (R$ 2.872295e+08). Todavia é a Primeira Quinzena que apresenta em média, maior volume de transações (47.293). Assim sendo, conclui-se que na Segunda Quinzena são realizadas menos transações (24.706) de valores mais altos comparativamente aos realizados na Primeira Quinzena.O montante da transação tem relação com período do dia que é executada, porque a noite (das 19 às 24h) os valores de transação são maiores (somatória R$ 1.552834e+08), enquanto de manhã (das 7 a 12h) os valores de transação são menores (somatória R$ 1.002308e+08). Sendo 50% maior o montante de transações da noite em relação a manhã. 
> Em relação as transações do tipo PIX, que começaram no final do ano 2020, elas passaram a ser a modalidade de envio e recebimento de dinheiro mais utilizadas, principalmente no mês de dezembro. Sendo que o DOC e o TED praticamente entraram em desuso de 2021 em diante. Por sua vez, a modalidade de compra de produtos e serviços mais utilizada foi compra no crédito, seguida por compra no débito. Fato que pode ser explicado pela facilidade nos últimos dos clientes anos adquirirem cartões de crédito via conta digital. Além disso, pode se dever as fato de o banco oferecer um aplicativo com interface amigável aos clientes, que os incentivam a controlar as compras e antecipar parcelas ganhando descontos na fatura do cartão.

### 📍 Status das propostas de crédito
> O tempo de vínculo com o banco dos clientes que pedem proposta financeira varia de 2 a 5 anos.
> E o Terceiro e Quarto Trimestre do ano concentram a grande maioria de número de envio da proposta e apresentam os maiores valores emprestados. Os cinco colaboradores com maior número propostas financeiras enviadas (da ordem de 1.000 propostas), com valores emprestados somados da ordem de R$5.800000e+09. E nota-se que os colaboradores com idade entre 30 e 60 anos concentram o maior volume de propostas.
> Em relação as agências, a Agência Digital é a agência com maior número de propostas de crédito enviada, da ordem de 1.000 propostas, com valor emprestado somado de R$ 4.114808e+10.

Por fim, com base nos resultados foram feitas recomendações à tomadores de decisão com base de insights acionáveis.
