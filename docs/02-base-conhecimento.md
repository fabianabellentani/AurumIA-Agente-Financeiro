# Base de Conhecimento

## Dados Utilizados

| Arquivo                     | Formato | Utilização no Agente                                                                               |
| --------------------------- | ------- | -------------------------------------------------------------------------------------------------- |
| `historico_atendimento.csv` | CSV     | Fornecer contexto sobre interações anteriores do cliente, permitindo respostas mais personalizadas |
| `perfil_investidor.json`    | JSON    | Identificar o perfil de risco do cliente e orientar recomendações financeiras adequadas            |
| `produtos_financeiros.json` | JSON    | Disponibilizar opções de produtos financeiros compatíveis com o perfil do cliente                  |
| `transacoes.csv`            | CSV     | Analisar o comportamento financeiro, padrões de gastos e possíveis oportunidades de melhoria       |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados mockados fornecidos foram utilizados sem alterações estruturais. No entanto, foram organizados e interpretados pelo agente para gerar insights relevantes, como categorização de gastos e identificação de padrões de consumo.

Essa abordagem garante a integridade dos dados originais, ao mesmo tempo em que permite ao agente extrair valor analítico a partir das informações disponíveis.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas abordagens para utilização da base de conhecimento pelo agente: a primeira consiste na inserção direta dos dados no prompt (injeção manual de contexto), enquanto a segunda envolve o carregamento dinâmico dos arquivos por meio de código em Python.

Neste projeto, optou-se pela segunda abordagem, permitindo maior escalabilidade, organização e reutilização dos dados durante a execução do agente.

Segue o código abaixo:

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/hitorico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para fins de simplificação neste protótipo, os dados foram inseridos diretamente no prompt, garantindo que o agente tenha acesso completo ao contexto do cliente durante a geração das respostas.

Em aplicações mais robustas, recomenda-se o carregamento dinâmico dessas informações, permitindo maior flexibilidade, escalabilidade e atualização em tempo real dos dados.

```text
DADOS DO CLIENTE (data/perfil_investidor.json):
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}

HISTÓRICO DE ATENDIMENTO (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

ÚLTIMAS TRANSAÇÕES (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

PRODUTOS DISPONÍVEIS (data/produtos_financeiros.json):
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]
```
---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto apresentado a seguir utiliza os dados da base de conhecimento, porém de forma resumida e estruturada, destacando apenas as informações mais relevantes para a análise.

Essa abordagem contribui para otimizar o uso de tokens, sem comprometer a qualidade das respostas.

Ainda assim, é importante garantir que o agente tenha acesso a todo o contexto necessário para uma tomada de decisão adequada.

```
Dados do Cliente:
- Nome: João Silva
- Idade: 32 anos
- Profissão: Analista de Sistemas
- Renda mensal: R$ 5.000
- Perfil de investidor: Moderado
- Objetivo principal: Construir reserva de emergência
- Patrimônio total: R$ 15.000
- Reserva atual: R$ 10.000

Metas:
- Completar reserva de emergência: R$ 15.000 até 06/2026
- Entrada de imóvel: R$ 50.000 até 12/2027

Resumo financeiro:
- Principal fonte de renda: Salário mensal
- Gastos relevantes:
  • Moradia: R$ 1.380
  • Alimentação: R$ 570
  • Transporte: R$ 295

Últimas interações:
- Interesse em CDB e Tesouro Selic
- Acompanhamento de metas financeiras

Produtos disponíveis:
- Tesouro Selic (baixo risco, ideal para reserva de emergência)
- CDB com liquidez diária (baixo risco, rendimento diário)
- Fundo multimercado (risco médio, diversificação)
...
```
