# Guia de Uso - LogisBrito

Este guia fornece instruções passo a passo para instalar, configurar e usar o sistema LogisBrito.

---

## Instalação de Dependências

### Opção 1: Usando `uv` (Recomendado)

`uv` é um gerenciador de pacotes Python ultrarrápido que simplifica a instalação de dependências.

#### Instalar `uv`

**Windows:**
```bash
pip install uv
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Criar Ambiente Virtual e Instalar Dependências

```bash
# Criar ambiente virtual
uv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências
uv pip install -r requirements.txt
```

### Opção 2: Usando `pip` Tradicional

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Verificar Instalação

```bash
python -c "import rdflib, owlrl; print('Instalação bem-sucedida!')"
```

---

## Executando o Notebook Passo a Passo

### 1. Iniciar Jupyter Lab

```bash
jupyter lab
```

Isso abrirá o Jupyter Lab no seu navegador padrão.

### 2. Abrir o Notebook Principal

Navegue até `notebooks/ontologia_conflito.ipynb` e abra o arquivo.

### 3. Executar as Células na Ordem

#### **Célula 1: Importações e Configuração**

```python
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
import owlrl
```

**Saída Esperada:** Nenhuma saída (importações silenciosas).

---

#### **Célula 2: Criar Schema da Ontologia**

Esta célula define as classes principais (AgenteUrbano, AcaoUrbana, etc.) e suas hierarquias.

**Saída Esperada:**
```
Schema criado com sucesso!
Total de triplas no schema: 45
```

---

#### **Célula 3: Adicionar Instâncias**

Esta célula adiciona as instâncias concretas do caso Coque (Prefeitura, Comunidade, ações, etc.).

**Saída Esperada:**
```
Instâncias adicionadas com sucesso!
Total de triplas na base de conhecimento: 78
```

---

#### **Célula 4: Salvar Base de Conhecimento**

```python
g.serialize(destination="../data/kb_conflito_urbano_final.ttl", format="turtle")
```

**Saída Esperada:**
```
Base de conhecimento salva em: data/kb_conflito_urbano_final.ttl
```

**Verificação:** O arquivo `data/kb_conflito_urbano_final.ttl` deve existir.

---

#### **Célula 5: Executar Inferência OWL DL**

```python
# Carregar base de conhecimento
g = Graph()
g.parse("../data/kb_conflito_urbano_final.ttl", format="turtle")

print(f"Triplas antes da inferência: {len(g)}")

# Executar reasoner
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

print(f"Triplas depois da inferência: {len(g)}")
print(f"Triplas inferidas: {len(g) - triplas_antes}")

# Salvar grafo inferido
g.serialize(destination="../data/kb_conflito_urbano_inferido.ttl", format="turtle")
```

**Saída Esperada:**
```
Triplas antes da inferência: 78
Triplas depois da inferência: 95
Triplas inferidas: 17

Grafo inferido salvo em: data/kb_conflito_urbano_inferido.ttl
```

**Interpretação:**
- O reasoner deduziu 17 novas triplas a partir das regras OWL.
- Exemplo de tripla inferida: `Prefeitura_do_Recife` é `AgenteUrbano` (inferido de `PoderPublico` ⊆ `AgenteUrbano`).

---

#### **Célula 6: Consulta SPARQL 1 - Atores Ambíguos**

```python
from src.sparql_queries import SPARQLQueryEngine

engine = SPARQLQueryEngine(g)
resultados = engine.query_ambiguous_actors()
print(engine.format_results(resultados))
```

**Saída Esperada:**
```
=== ATORES AMBÍGUOS ===

Ator: Prefeitura do Recife
  Ação Propositiva: Propor Lei PREZEIS 1995
  Ação Impeditiva: Sancionar Lei do Remembramento 2020
  Ação Impeditiva: Omitir Fiscalização PREZEIS

Total de atores ambíguos encontrados: 1
```

**Interpretação:**
- A Prefeitura executa ações contraditórias: protege o Coque (PREZEIS) mas também facilita gentrificação (Remembramento).
- Isso revela a **ambiguidade do poder público** no conflito urbano.

---

#### **Célula 7: Consulta SPARQL 2 - Causalidade de Danos**

```python
resultados = engine.query_causality_chain()
print(engine.format_results(resultados))
```

**Saída Esperada:**
```
=== CADEIA DE CAUSALIDADE ===

Agente: Prefeitura do Recife
  Ação: Sancionar Lei do Remembramento 2020
  → Causa: Risco de Gentrificação Coque

Agente: Prefeitura do Recife
  Ação: Omitir Fiscalização PREZEIS
  → Causa: Risco de Gentrificação Coque

Agente: Agentes Especulativos da Orla
  Ação: Sancionar Lei do Remembramento 2020
  → Causa: Risco de Gentrificação Coque

Total de cadeias causais encontradas: 3
```

**Interpretação:**
- Três ações impeditivas causam o mesmo dano: risco de gentrificação.
- A Prefeitura e os especuladores compartilham responsabilidade causal.

---

#### **Célula 8: Consulta SPARQL 3 - Conflito de Instrumentos**

```python
resultados = engine.query_conflicting_instruments()
print(engine.format_results(resultados))
```

**Saída Esperada:**
```
=== INSTRUMENTOS EM CONFLITO ===

Dano: Risco de Gentrificação Coque
  Instrumento Protetor: Lei PREZEIS 1995 (Ação Propositiva)
  Instrumento Agressor: Lei do Remembramento 2020 (Ação Impeditiva)

⚠️ CONFLITO LÓGICO DETECTADO: Dois instrumentos legais atuam em direções opostas sobre o mesmo dano.

Total de conflitos identificados: 1
```

**Interpretação:**
- Duas leis municipais estão em conflito direto.
- PREZEIS protege ZEIS, mas Remembramento facilita sua destruição.
- Isso evidencia **contradição legislativa**.

---

## Interpretação dos Resultados

### Consulta 1: Atores Ambíguos

**O que significa?**
- Identifica agentes que executam ações de classes opostas (propositiva E impeditiva).
- No caso do Coque, a Prefeitura age de forma contraditória.

**Por que é importante?**
- Revela **incoerência política**: o mesmo ator protege e ameaça a comunidade.
- Permite questionar a legitimidade das ações do poder público.

### Consulta 2: Causalidade de Danos

**O que significa?**
- Rastreia quem causa quais danos e através de quais ações.
- Mapeia a **cadeia de responsabilidade**.

**Por que é importante?**
- Permite atribuir responsabilidade causal a agentes específicos.
- Facilita argumentação jurídica e advocacy.

### Consulta 3: Conflito de Instrumentos

**O que significa?**
- Identifica instrumentos legais que atuam em direções opostas sobre o mesmo dano.
- Detecta **contradições legislativas**.

**Por que é importante?**
- Evidencia falhas no sistema legal.
- Permite propor revogação ou harmonização de leis conflitantes.

---

## Usando os Módulos Python Programaticamente

### Exemplo 1: Executar Consultas Customizadas

```python
from rdflib import Graph
from src.sparql_queries import SPARQLQueryEngine

# Carregar grafo inferido
g = Graph()
g.parse("data/kb_conflito_urbano_inferido.ttl", format="turtle")

# Criar engine
engine = SPARQLQueryEngine(g)

# Executar consulta customizada
query = """
PREFIX rec: <http://recife.leg.br/ontologia-conflito#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?agente ?label
WHERE {
    ?agente a rec:PoderPublico ;
            rdfs:label ?label .
}
"""

resultados = g.query(query)
for row in resultados:
    print(f"Poder Público: {row.label}")
```

### Exemplo 2: Validar Ontologia

```python
from src.validators import OntologyValidator

# Criar validador
validator = OntologyValidator(g)

# Validar classes esperadas
classes_esperadas = [
    "AgenteUrbano",
    "AcaoUrbana",
    "DanoUrbano",
    "BeneficioUrbano"
]

resultado = validator.validate_classes(classes_esperadas)
if resultado.is_valid:
    print("✓ Todas as classes esperadas estão presentes")
else:
    print("✗ Classes faltando:", resultado.errors)

# Gerar relatório completo
relatorio = validator.generate_report()
print(relatorio)
```

---

## Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'owlrl'`

**Causa:** Dependência não instalada.

**Solução:**
```bash
pip install owlrl
# ou
uv pip install owlrl
```

---

### Erro: `FileNotFoundError: [Errno 2] No such file or directory: 'data/kb_conflito_urbano_final.ttl'`

**Causa:** Base de conhecimento não foi gerada.

**Solução:**
1. Execute o notebook `ontologia_conflito.ipynb` completamente.
2. Verifique se o arquivo foi criado em `data/kb_conflito_urbano_final.ttl`.

---

### Erro: `ParseException: Expected end of text, found '.'`

**Causa:** Erro de sintaxe no arquivo Turtle.

**Solução:**
1. Valide o arquivo em http://ttl.summerofcode.be/
2. Verifique se há pontos finais faltando ou duplicados.
3. Verifique se todos os prefixos estão definidos.

---

### Aviso: `UserWarning: Reasoner took longer than expected`

**Causa:** Grafo muito grande ou regras complexas.

**Solução:**
- Para este projeto (≈100 triplas), inferência deve ser instantânea.
- Se o aviso aparecer, verifique se há loops infinitos nas regras OWL.

---

### Consulta SPARQL Retorna Vazio

**Causa:** Prefixos incorretos ou grafo não inferido.

**Solução:**
1. Verifique se está usando o grafo **inferido** (`kb_conflito_urbano_inferido.ttl`).
2. Verifique se os prefixos na consulta correspondem aos do grafo:
   ```python
   print(list(g.namespaces()))
   ```
3. Execute a inferência antes de consultar.

---

### Erro: `Inconsistent ontology detected`

**Causa:** Instância viola restrições `disjointWith`.

**Solução:**
1. Identifique a instância problemática no erro.
2. Verifique se ela está declarada como membro de classes disjuntas.
3. Corrija a modelagem removendo uma das declarações.

---

## Executando Testes Automatizados

```bash
# Executar todos os testes
pytest tests/ -v

# Executar teste específico
pytest tests/test_ontologia.py::test_schema_classes -v

# Gerar relatório de cobertura
pytest tests/ --cov=src --cov-report=html
```

**Saída Esperada:**
```
tests/test_ontologia.py::test_schema_loads PASSED
tests/test_ontologia.py::test_schema_classes PASSED
tests/test_ontologia.py::test_object_properties PASSED
tests/test_ontologia.py::test_disjoint_constraints PASSED
tests/test_ontologia.py::test_instances_typing PASSED
tests/test_ontologia.py::test_sparql_ambiguous_actors PASSED
tests/test_ontologia.py::test_sparql_causality PASSED

======================== 7 passed in 2.34s ========================
```

---

## Próximos Passos

Após dominar o uso básico, você pode:

1. **Adicionar Novos Casos:** Modele outros conflitos urbanos de Recife (ex: Brasília Teimosa, Cais José Estelita).
2. **Criar Novas Consultas:** Implemente queries SPARQL customizadas para suas perguntas de pesquisa.
3. **Integrar com Dados Geoespaciais:** Conecte a ontologia com shapefiles de ZEIS.
4. **Desenvolver Interface Web:** Crie uma aplicação Flask/Django para consultas interativas.

---

## Recursos Adicionais

- **Tutorial RDFLib:** https://rdflib.readthedocs.io/
- **Tutorial SPARQL:** https://www.w3.org/TR/sparql11-query/
- **OWL 2 Primer:** https://www.w3.org/TR/owl2-primer/
- **Documentação owlrl:** https://owl-rl.readthedocs.io/
