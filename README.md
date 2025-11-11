# LogisBrito: A Logical Oracle for Recife's Urban Legislation

**Project Status:** Initial Research & Development | University Project (CIN-UFPE)

## About the Project

`LogisBrito` is a proof-of-concept expert system designed to serve as a **decision-support tool for urban and social policy** in Recife, Brazil. Named after the visionary urbanist Saturnino de Brito, this project aims to create a logical and auditable knowledge base from the city's complex web of urban legislation.

Our primary goal is to address critical urban challenges, such as the requalification of at-risk social housing zones (ZEIS) and the sustainable regeneration of underutilized historical areas, like the Santo Antônio neighborhood.

## The Core Problem

Recife's urban development is governed by layers of historical master plans, decrees, and preservation laws. This legal framework is complex, often contradictory, and inaccessible to citizens, architects, and even technical staff. Answering a seemingly simple question like "What incentives are available to sustainably retrofit this specific historical building for social housing?" can require weeks of legal research.

Probabilistic models like LLMs are ill-suited for this domain, as they cannot guarantee factual accuracy, provide auditable reasoning, or detect logical conflicts within the legal code—risks that are unacceptable when dealing with legal compliance and public policy.

## Our Approach: Logic over LLMs

This project takes a **symbolic AI** approach, building a knowledge graph based on the **Web Ontology Language (OWL DL)**.

Instead of generating probable text, our system:
1.  **Represents** urban laws as a set of precise, logical facts and rules.
2.  **Uses** a reasoner to make logical deductions based on this knowledge.
3.  **Provides** answers that are fully auditable, tracing every conclusion back to the specific article of law it originated from.
4.  **Enables** "what-if" policy simulations, allowing users to see the logical impact of introducing a new rule or incentive.

This makes the `LogisBrito` a **verifiable oracle**, not a conversational generator.

## Technology Stack

* **Language:** Python
* **Knowledge Representation:** `rdflib` for building the RDF graph and modeling the OWL ontology.
* **Reasoning:** `owlrl` for OWL DL inference and logical deduction.
* **Query Language:** SPARQL for querying the knowledge base.
* **Testing:** `pytest` for automated validation of ontology integrity.
* **Prototyping:** JupyterLab

## Progresso Atual

O projeto LogisBrito está em fase de desenvolvimento ativo com os seguintes componentes implementados:

### ✅ Concluído
- **Schema da Ontologia (v4):** Estrutura completa com 6 eixos conceituais (Agentes, Ações, Instrumentos, Espaços, Danos, Benefícios)
- **Base de Conhecimento:** Instâncias modelando o conflito urbano do Coque (gentrificação vs. preservação)
- **Inferência OWL DL:** Motor de raciocínio lógico usando `owlrl` para deduzir novos fatos
- **Consultas SPARQL:** Queries para extrair narrativas de conflito (atores ambíguos, causalidade, instrumentos conflitantes)
- **Módulos Python Reutilizáveis:** `sparql_queries.py` e `validators.py` para análise programática
- **Testes Automatizados:** Suite pytest validando integridade do schema e instâncias

### 🚧 Em Desenvolvimento
- **Documentação Técnica:** Guias de arquitetura, uso e resultados
- **Validação Final:** Execução completa do pipeline e verificação de resultados

### 📋 Próximos Passos
- Expandir base de conhecimento com mais casos de conflito urbano
- Implementar interface web para consultas interativas
- Integrar com dados geoespaciais de Recife

## Estrutura do Projeto

```
LogisBrito/
├── data/                                    # Arquivos de ontologia e base de conhecimento
│   ├── ontologia_conflito_urbano_schema_v4.ttl   # Schema OWL DL (classes, propriedades, restrições)
│   ├── kb_conflito_urbano_final.ttl              # Base de conhecimento com instâncias
│   └── kb_conflito_urbano_inferido.ttl           # Grafo expandido após inferência
├── notebooks/                               # Notebooks Jupyter para prototipagem
│   ├── ontologia_conflito.ipynb                  # Criação do schema e instâncias
│   └── oraculo_de_brito_visualizacao.html        # Visualização do grafo
├── src/                                     # Módulos Python reutilizáveis
│   ├── sparql_queries.py                         # Engine de consultas SPARQL
│   └── validators.py                             # Validadores de integridade da ontologia
├── tests/                                   # Testes automatizados
│   └── test_ontologia.py                         # Suite pytest para validação
├── docs/                                    # Documentação técnica
│   ├── ARCHITECTURE.md                           # Estrutura da ontologia
│   ├── USAGE_GUIDE.md                            # Guia de uso
│   └── RESULTADOS.md                             # Resultados e análises
├── README.md                                # Este arquivo
├── SOURCES.md                               # Fontes e referências
└── requirements.txt                         # Dependências Python
```

## Como Usar

### 1. Instalação de Dependências

Recomendamos usar `uv` para gerenciamento rápido de dependências:

```bash
# Instalar uv (se ainda não tiver)
pip install uv

# Criar ambiente virtual e instalar dependências
uv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
uv pip install -r requirements.txt
```

Alternativamente, use pip tradicional:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Executar o Notebook Principal

```bash
jupyter lab notebooks/ontologia_conflito.ipynb
```

Execute as células na ordem para:
1. Criar o schema da ontologia
2. Adicionar instâncias do caso Coque
3. Executar inferência OWL DL
4. Executar consultas SPARQL para extrair narrativas

### 3. Executar Testes Automatizados

```bash
pytest tests/ -v
```

Os testes validam:
- Integridade do schema (classes, propriedades, restrições)
- Tipagem correta das instâncias
- Funcionamento das consultas SPARQL
- Resultados esperados da inferência

### 4. Usar Módulos Python Programaticamente

```python
from rdflib import Graph
from src.sparql_queries import SPARQLQueryEngine
from src.validators import OntologyValidator

# Carregar base de conhecimento inferida
g = Graph()
g.parse("data/kb_conflito_urbano_inferido.ttl", format="turtle")

# Executar consultas
engine = SPARQLQueryEngine(g)
atores_ambiguos = engine.query_ambiguous_actors()
print(engine.format_results(atores_ambiguos))

# Validar ontologia
validator = OntologyValidator(g)
report = validator.generate_report()
print(report)
```

Para mais detalhes, consulte a [documentação técnica](docs/USAGE_GUIDE.md).
