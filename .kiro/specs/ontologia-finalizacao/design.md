# Design Document

## Overview

O design da finalização do LogisBrito segue uma arquitetura modular baseada em notebooks Jupyter, onde cada notebook tem uma responsabilidade específica: (1) criação do schema e instâncias, (2) inferência lógica, (3) consultas SPARQL, e (4) testes. A solução utiliza a biblioteca `owlrl` para inferência OWL DL e `rdflib` para manipulação de grafos RDF e execução de consultas SPARQL.

## Architecture

### Componentes Principais

```
LogisBrito/
├── data/
│   ├── ontologia_conflito_urbano_schema_v4.ttl (existente)
│   ├── kb_conflito_urbano_final.ttl (existente)
│   └── kb_conflito_urbano_inferido.ttl (novo - gerado pela inferência)
├── notebooks/
│   ├── ontologia_conflito.ipynb (existente - criação do schema)
│   ├── 02_Inferencia_e_Consulta.ipynb (novo)
│   └── 03_Testes_Ontologia.ipynb (novo)
├── src/
│   ├── __init__.py
│   ├── inference_engine.py (novo - módulo de inferência)
│   ├── sparql_queries.py (novo - consultas reutilizáveis)
│   └── validators.py (novo - validadores de ontologia)
├── tests/
│   └── test_ontologia.py (novo - testes pytest)
└── docs/
    ├── ARCHITECTURE.md (novo)
    └── USAGE_GUIDE.md (novo)
```

### Fluxo de Dados

1. **Schema + Instâncias** → `kb_conflito_urbano_final.ttl`
2. **Reasoner OWL** → `kb_conflito_urbano_inferido.ttl` (grafo expandido)
3. **Consultas SPARQL** → Resultados formatados (narrativas de conflito)
4. **Validadores** → Relatórios de integridade

## Components and Interfaces

### 1. Módulo de Inferência (`src/inference_engine.py`)

**Responsabilidade:** Encapsular a lógica de inferência OWL DL.

**Interface:**
```python
class InferenceEngine:
    def __init__(self, kb_path: str):
        """Carrega a base de conhecimento"""
        
    def run_inference(self) -> Graph:
        """Executa o reasoner OWL DL e retorna o grafo expandido"""
        
    def save_inferred_graph(self, output_path: str) -> None:
        """Salva o grafo inferido em arquivo"""
        
    def get_statistics(self) -> dict:
        """Retorna estatísticas (triplas antes/depois, tempo de execução)"""
```

**Dependências:**
- `rdflib.Graph`
- `owlrl.DeductiveClosure`
- `owlrl.OWLRL_Semantics`

### 2. Módulo de Consultas SPARQL (`src/sparql_queries.py`)

**Responsabilidade:** Definir e executar consultas SPARQL reutilizáveis.

**Interface:**
```python
class SPARQLQueryEngine:
    def __init__(self, graph: Graph):
        """Inicializa com um grafo RDF"""
        
    def query_ambiguous_actors(self) -> List[dict]:
        """Identifica atores executando ações opostas"""
        
    def query_causality_chain(self, dano_uri: str) -> List[dict]:
        """Rastreia cadeia de causalidade de um dano específico"""
        
    def query_conflicting_instruments(self) -> List[dict]:
        """Identifica instrumentos em conflito sobre o mesmo dano"""
        
    def format_results(self, results: List[dict]) -> str:
        """Formata resultados para exibição legível"""
```

**Consultas Implementadas:**

1. **Atores Ambíguos:**
```sparql
SELECT ?ator_label ?acao_propositiva_label ?acao_impeditiva_label
WHERE {
    ?ator a rec:AgenteUrbano ;
          rdfs:label ?ator_label ;
          rec:executaAcao ?acao_propositiva ;
          rec:executaAcao ?acao_impeditiva .
    ?acao_propositiva a rec:Acao_Propositiva ;
                      rdfs:label ?acao_propositiva_label .
    ?acao_impeditiva a rec:Acao_Impeditiva ;
                     rdfs:label ?acao_impeditiva_label .
}
```

2. **Causalidade de Dano:**
```sparql
SELECT ?agente_label ?acao_label ?dano_label
WHERE {
    ?acao a rec:Acao_Impeditiva ;
          rec:causa_direta ?dano ;
          rdfs:label ?acao_label .
    ?agente rec:executaAcao ?acao ;
            rdfs:label ?agente_label .
    ?dano rdfs:label ?dano_label .
}
```

3. **Conflito de Instrumentos:**
```sparql
SELECT ?dano_label ?acao_positiva_label ?acao_negativa_label
WHERE {
    ?dano a rec:DanoUrbano ;
          rdfs:label ?dano_label .
    ?acao_positiva rec:reverte_por_forca ?dano ;
                   a rec:Acao_Propositiva ;
                   rdfs:label ?acao_positiva_label .
    ?acao_negativa rec:causa_direta ?dano ;
                   a rec:Acao_Impeditiva ;
                   rdfs:label ?acao_negativa_label .
}
```

### 3. Módulo de Validação (`src/validators.py`)

**Responsabilidade:** Validar integridade do schema e instâncias.

**Interface:**
```python
class OntologyValidator:
    def __init__(self, graph: Graph):
        """Inicializa com um grafo RDF"""
        
    def validate_syntax(self) -> ValidationResult:
        """Valida sintaxe Turtle"""
        
    def validate_classes(self, expected_classes: List[str]) -> ValidationResult:
        """Valida presença de classes esperadas"""
        
    def validate_properties(self) -> ValidationResult:
        """Valida propriedades de objeto e suas restrições"""
        
    def validate_disjointness(self) -> ValidationResult:
        """Valida restrições disjointWith"""
        
    def validate_instances(self) -> ValidationResult:
        """Valida tipagem de instâncias"""
        
    def generate_report(self) -> str:
        """Gera relatório completo de validação"""
```

### 4. Notebook de Inferência (`notebooks/02_Inferencia_e_Consulta.ipynb`)

**Estrutura:**

**Célula 1: Inferência**
- Carrega `kb_conflito_urbano_final.ttl`
- Executa `owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)`
- Salva `kb_conflito_urbano_inferido.ttl`
- Exibe estatísticas (triplas antes/depois)

**Célula 2: Consulta 1 - Atores Ambíguos**
- Executa consulta SPARQL
- Formata e exibe resultados

**Célula 3: Consulta 2 - Causalidade**
- Executa consulta SPARQL
- Formata e exibe resultados

**Célula 4: Consulta 3 - Conflito de Instrumentos**
- Executa consulta SPARQL
- Formata e exibe resultados

### 5. Notebook de Testes (`notebooks/03_Testes_Ontologia.ipynb`)

**Estrutura:**

**Célula 1: Validação de Schema**
- Carrega schema
- Valida classes principais
- Valida propriedades

**Célula 2: Validação de Instâncias**
- Carrega KB completa
- Valida tipagem de instâncias
- Valida relações

**Célula 3: Validação de Inferência**
- Carrega KB inferida
- Valida triplas inferidas esperadas
- Compara com KB original

## Data Models

### Grafo RDF

O grafo RDF segue o modelo de triplas (sujeito, predicado, objeto):

```
<http://recife.leg.br/ontologia-conflito#Prefeitura_do_Recife>
    rdf:type rec:PoderPublico ;
    rdfs:label "Prefeitura do Recife" ;
    rec:executaAcao rec:Acao_Propor_Lei_PREZEIS_1995 ;
    rec:executaAcao rec:Acao_Sancionar_Lei_18772_2020 .
```

### Resultado de Consulta SPARQL

```python
{
    "ator_label": "Prefeitura do Recife",
    "acao_propositiva_label": "Propor Lei PREZEIS 1995",
    "acao_impeditiva_label": "Sancionar Lei do Remembramento 2020"
}
```

### Resultado de Validação

```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    details: dict
```

## Error Handling

### Estratégias de Tratamento de Erros

1. **Erro de Carregamento de Arquivo:**
   - Verificar existência do arquivo antes de carregar
   - Exibir mensagem clara indicando o arquivo faltante
   - Sugerir executar notebook anterior se necessário

2. **Erro de Sintaxe Turtle:**
   - Capturar exceções de parsing
   - Exibir linha e coluna do erro
   - Sugerir validação online (e.g., http://ttl.summerofcode.be/)

3. **Erro de Consulta SPARQL:**
   - Validar sintaxe da consulta antes de executar
   - Capturar exceções de execução
   - Exibir consulta problemática para debug

4. **Erro de Inferência:**
   - Capturar exceções do reasoner
   - Verificar se há inconsistências lógicas no grafo
   - Exibir detalhes da inconsistência encontrada

### Exemplo de Implementação

```python
def load_knowledge_base(path: str) -> Graph:
    """Carrega base de conhecimento com tratamento de erros"""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Arquivo '{path}' não encontrado. "
            f"Execute o notebook 'ontologia_conflito.ipynb' primeiro."
        )
    
    try:
        g = Graph()
        g.parse(path, format="turtle")
        return g
    except Exception as e:
        raise ValueError(
            f"Erro ao carregar '{path}': {str(e)}\n"
            f"Verifique a sintaxe Turtle do arquivo."
        )
```

## Testing Strategy

### Níveis de Teste

1. **Testes de Unidade (pytest):**
   - Testar funções individuais de validação
   - Testar parsing de consultas SPARQL
   - Testar formatação de resultados

2. **Testes de Integração (notebooks):**
   - Testar fluxo completo: schema → instâncias → inferência → consultas
   - Validar que triplas esperadas são inferidas
   - Validar que consultas retornam resultados esperados

3. **Testes de Validação (validators):**
   - Validar integridade do schema
   - Validar consistência das instâncias
   - Validar ausência de inconsistências lógicas

### Casos de Teste Principais

**Teste 1: Inferência de Subclasse**
- **Dado:** Instância `rec:Prefeitura_do_Recife` tipada como `rec:PoderPublico`
- **Quando:** Reasoner é executado
- **Então:** Tripla `(rec:Prefeitura_do_Recife, rdf:type, rec:AgenteUrbano)` deve ser inferida

**Teste 2: Consulta de Atores Ambíguos**
- **Dado:** Prefeitura executa ação propositiva E impeditiva
- **Quando:** Consulta SPARQL é executada
- **Então:** Prefeitura deve aparecer nos resultados

**Teste 3: Validação de Disjointness**
- **Dado:** Schema define `Acao_Propositiva` disjoint com `Acao_Impeditiva`
- **Quando:** Validador é executado
- **Então:** Restrição deve ser confirmada

**Teste 4: Detecção de Inconsistência**
- **Dado:** Instância tipada como ambas classes disjuntas
- **Quando:** Reasoner é executado
- **Então:** Inconsistência deve ser detectada

### Ferramentas de Teste

- **pytest:** Testes automatizados em Python
- **rdflib:** Validação de sintaxe e estrutura
- **owlrl:** Validação de consistência lógica

## Implementation Notes

### Dependências Adicionais

Adicionar ao `requirements.txt`:
```
owlrl>=6.0.2
pytest>=7.4.0
```

### Ordem de Implementação

1. Instalar `owlrl`: `pip install owlrl`
2. Criar módulos em `src/`
3. Criar notebook `02_Inferencia_e_Consulta.ipynb`
4. Criar notebook `03_Testes_Ontologia.ipynb`
5. Criar testes pytest em `tests/`
6. Atualizar documentação

### Considerações de Performance

- Inferência OWL DL pode ser lenta para grafos grandes (>10k triplas)
- Para este projeto (≈100 triplas), inferência deve ser instantânea
- Consultas SPARQL são eficientes para este tamanho de grafo

### Extensibilidade

O design permite fácil adição de:
- Novas consultas SPARQL (adicionar método em `SPARQLQueryEngine`)
- Novos validadores (adicionar método em `OntologyValidator`)
- Novos reasoners (substituir `owlrl` por Pellet, HermiT, etc.)
