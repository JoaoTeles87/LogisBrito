# LogisBrito: Um Oráculo Lógico para a Legislação Urbana do Recife

**Status do Projeto:** Prova de Conceito (Arquitetura V5 Estável) | Projeto Acadêmico (CIn-UFPE)

## Sobre o Projeto

`LogisBrito` é um sistema especialista e prova de conceito, desenhado para servir como uma **ferramenta de apoio à decisão para políticas urbanas e sociais** na cidade do Recife. Nomeado em homenagem ao urbanista visionário Saturnino de Brito, este projeto visa criar uma base de conhecimento lógica e auditável a partir da complexa teia de legislação urbana da cidade.

## O Problema Central

O desenvolvimento urbano do Recife é governado por camadas de planos diretores históricos, decretos e leis de preservação. Esta estrutura legal é complexa, muitas vezes contraditória e inacessível a cidadãos, arquitetos e até mesmo ao corpo técnico da prefeitura.

Modelos probabilísticos como LLMs são inadequados para este domínio, pois não podem garantir precisão factual, fornecer raciocínio auditável ou detectar conflitos lógicos dentro do código legal — riscos inaceitáveis ao lidar com conformidade legal e políticas públicas.

## Nossa Abordagem: Lógica sobre LLMs

Este projeto adota uma abordagem de **IA simbólica**, construindo um grafo de conhecimento baseado na **Web Ontology Language (OWL DL)**.

Em vez de gerar texto provável, nosso sistema:
1.  **Representa** as leis urbanas como um conjunto de fatos e regras lógicas e precisas.
2.  **Usa** um reasoner (inferidor) para fazer deduções lógicas com base nesse conhecimento.
3.  **Fornece** respostas que são totalmente auditáveis, rastreando cada conclusão até o artigo de lei específico de onde se originou.

Isso torna o `LogisBrito` um **oráculo verificável**, e não um gerador conversacional.

---

## Arquitetura (Schema V5)

A versão atual da ontologia (V5) modela o conflito urbano através de eixos principais: **Agentes**, **Ações**, **Danos/Benefícios** e **Normas**.

A inovação chave do Schema V5 é a introdução da classe `Norma` e da propriedade simétrica `rec:conflitaCom`. Isso nos permite modelar explicitamente conflitos lógicos entre diferentes instrumentos legais, como duas leis que se contradizem.

Classes principais:
- `AgenteUrbano`
  - `PoderPublico`
    - `AgenteExecutivo` (ex: Prefeitura)
    - `AgenteLegislativo` (ex: Câmara Municipal)
- `AcaoUrbana`
  - `Acao_Propositiva` (gera benefício)
  - `Acao_Impeditiva` (causa dano)
- `Norma`
  - `LegislacaoUrbana` (ex: Leis, Decretos)
- `DanoUrbano` e `BeneficioUrbano`

## Como Usar (Guia Rápido)

A arquitetura do projeto segue o princípio de **"Pipeline como Código"**. A lógica de construção da base de conhecimento está em scripts Python, e o notebook Jupyter é usado para orquestração e análise.

#### 1. Instalação
Clone o repositório e instale as dependências:
```bash
pip install -r requirements.txt
```

#### 2. Executando a Pipeline
Abra e execute o notebook principal:
`notebooks/ontologia_conflito.ipynb`

O notebook é autoexplicativo e está dividido em passos:
- **Passo 1:** Executa o script `src/build_knowledge_base.py`, que automaticamente gera o schema, popula as instâncias e executa a inferência, salvando os resultados em `data/`.
- **Passo 2:** Carrega o grafo final já inferido (`kb_conflito_v5_inferido.ttl`).
- **Passo 3:** Executa as consultas SPARQL para extrair os insights e provar as hipóteses de conflito.
- **Passo 4:** Gera uma visualização interativa do grafo de conhecimento.

## Resultados da Análise (V5)

A execução da pipeline no notebook prova as seguintes narrativas de conflito:

1.  **Conflito Normativo Explícito**: A consulta SPARQL que utiliza a propriedade `rec:conflitaCom` **prova um conflito direto** entre a `Lei do PREZEIS (1995)` e a `Lei do Remembramento (2020)`.

2.  **Cadeia de Causalidade de Dano**: A análise do grafo demonstra que a `Prefeitura do Recife` (AgenteExecutivo), ao executar a `Ação de Sancionar a Lei do Remembramento` (Ação Impeditiva), causa diretamente um `Risco de Gentrificação` (Dano Urbano).

## Como Testar a Pipeline

O projeto possui uma suíte de testes automatizada que valida toda a pipeline, desde a execução do script de build até a verificação dos resultados das consultas SPARQL.

Para rodar os testes, execute na raiz do projeto:
```bash
python -m pytest -v tests/test_ontologia.py
```

## Tecnologias Utilizadas
* **Linguagem:** Python
* **Base de Conhecimento:** `rdflib` para modelagem RDF/OWL.
* **Inferência:** `owlrl` para inferência OWL 2 RL.
* **Consultas:** SPARQL para consultar o grafo.
* **Testes:** `pytest` para testes automatizados da pipeline.
* **Análise e Orquestração:** JupyterLab
* **Visualização:** `pyvis` para visualização de grafos.