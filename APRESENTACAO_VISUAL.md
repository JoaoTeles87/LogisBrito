# 📊 GUIA DE APRESENTAÇÃO VISUAL

## 🎯 Como Usar as Visualizações para Explicar o Trabalho

Este guia mostra como usar cada visualização para explicar aspectos técnicos da ontologia ao professor.

---

## 📋 PREPARAÇÃO

### 1. Instalar Bibliotecas de Visualização

```bash
pip install networkx matplotlib pyvis
```

### 2. Gerar Todas as Visualizações

```bash
python visualize_ontology.py
```

Isso criará 5 arquivos na pasta `visualizations/`:
- ✅ `class_hierarchy.png` - Hierarquia de classes
- ✅ `ontology_interactive.html` - Grafo interativo
- ✅ `statistics.png` - Estatísticas do sistema
- ✅ `axioms_diagram.png` - Diagramas dos axiomas
- ✅ `architecture.png` - Arquitetura do sistema

---

## 🎨 ROTEIRO DE APRESENTAÇÃO

### SLIDE 1: Arquitetura do Sistema
**Arquivo:** `visualizations/architecture.png`

**O que mostrar:**
```
"O sistema tem 4 camadas principais:

1. SCHEMA (Azul) - A ontologia base com 7 eixos temáticos
   • 40+ classes organizadas hierarquicamente
   • 25+ propriedades que conectam conceitos
   • 20+ axiomas formais que garantem consistência

2. INSTÂNCIAS (Vermelho) - Casos reais do Recife
   • Conflito PREZEIS vs Remembramento
   • 30+ indivíduos (leis, agentes, espaços)
   • Relações causais explícitas

3. REASONER (Amarelo) - Inferência automática
   • OWL-RL expande 332 → 1083 triplas
   • 751 novas triplas inferidas
   • Tempo: 0.17 segundos

4. CONSULTAS (Verde) - Análise semântica
   • 10 consultas SPARQL avançadas
   • Detecção automática de conflitos
   • Rastreamento de causalidade
"
```

**Ponto técnico chave:**
"Isso não é um banco de dados comum. É uma base de conhecimento com raciocínio lógico automático."

---

### SLIDE 2: Hierarquia de Classes
**Arquivo:** `visualizations/class_hierarchy.png`

**O que mostrar:**
```
"A ontologia modela 7 eixos temáticos:

1. AGENTES URBANOS (vermelho)
   • Fragmentação do poder público em 5 tipos
   • Comunidades e agentes de mercado
   • Modelagem de papéis antagônicos

2. AÇÕES URBANAS (azul)
   • Dicotomia: Propositivas vs Impeditivas
   • Axioma de disjunção garante exclusividade

3. ESPAÇOS (verde)
   • ZEIS, Centro Ocioso, Zonas de Preservação
   • Sobreposição legal modelada

4. INSTRUMENTOS (laranja)
   • PEUC, TDC, Remembramento
   • Classificação por tipo

5. DANOS e BENEFÍCIOS (roxo/verde)
   • Mutuamente exclusivos (axioma)
   • Relações de reversão

6. NORMAS (amarelo)
   • Leis, projetos, artigos
   • Conflitos formalizados
"
```

**Ponto técnico chave:**
"Cada seta representa uma relação rdfs:subClassOf. O reasoner propaga tipos automaticamente pela hierarquia."

---

### SLIDE 3: Axiomas Formais
**Arquivo:** `visualizations/axioms_diagram.png`

**O que mostrar (apontando para cada quadrante):**

**Quadrante 1 (Superior Esquerdo):**
```
"AXIOMA DE DISJUNÇÃO
• Acao_Propositiva ⊥ Acao_Impeditiva
• Garante que uma ação não pode ser positiva E negativa
• Permite detectar contradições no modelo
• Exemplo: Se tentarmos classificar 'Criar PREZEIS' como impeditiva,
  o reasoner detecta inconsistência"
```

**Quadrante 2 (Superior Direito):**
```
"PROPRIEDADE SIMÉTRICA
• conflitaCom(A, B) → conflitaCom(B, A)
• Declaramos apenas uma direção
• O reasoner infere a direção oposta automaticamente
• Exemplo: Lei PREZEIS conflita com Remembramento
  → Remembramento conflita com PREZEIS (inferido)"
```

**Quadrante 3 (Inferior Esquerdo):**
```
"PROPRIEDADE TRANSITIVA
• coincideCom(A,B) ∧ coincideCom(B,C) → coincideCom(A,C)
• Modela sobreposição legal através de múltiplas camadas
• Exemplo: IEP está em ZEPH, ZEPH está em Área Recentro
  → IEP está em Área Recentro (inferido)
• Detecta conflitos de jurisdição automaticamente"
```

**Quadrante 4 (Inferior Direito):**
```
"RESTRIÇÕES DE DOMÍNIO/RANGE
• causa_direta: domain = Acao_Impeditiva, range = DanoUrbano
• Valida automaticamente a consistência
• Exemplo: Se X causa_direta Y, então:
  - X é inferido como Acao_Impeditiva
  - Y é inferido como DanoUrbano
• Impossível criar relações inválidas"
```

**Ponto técnico chave:**
"Estes axiomas transformam a ontologia de um simples modelo de dados em uma base de conhecimento com raciocínio lógico."

---

### SLIDE 4: Estatísticas de Inferência
**Arquivo:** `visualizations/statistics.png`

**O que mostrar (gráfico de barras):**
```
"EVOLUÇÃO DA BASE DE CONHECIMENTO

1. Schema (236 triplas)
   • Definições de classes
   • Propriedades
   • Axiomas formais

2. Instâncias (332 triplas)
   • Schema + casos reais
   • 96 triplas de instâncias explícitas

3. Inferido (1083 triplas)
   • Após aplicar o reasoner OWL-RL
   • 751 novas triplas descobertas
   • Taxa de inferência: 3.3x
"
```

**O que mostrar (gráfico de pizza):**
```
"COMPOSIÇÃO DO GRAFO FINAL

• 21.8% - Axiomas e definições (schema)
• 8.9% - Instâncias explícitas (casos)
• 69.3% - Triplas inferidas (conhecimento novo)

Isso significa que 70% do conhecimento no sistema
foi DESCOBERTO AUTOMATICAMENTE pelo reasoner!"
```

**Ponto técnico chave:**
"O reasoner não apenas armazena dados - ele DESCOBRE conhecimento novo através de raciocínio lógico."

---

### SLIDE 5: Grafo Interativo
**Arquivo:** `visualizations/ontology_interactive.html`

**Como usar:**
1. Abra o arquivo HTML no navegador
2. Use o mouse para:
   - Arrastar nós
   - Zoom in/out
   - Clicar em nós para destacar conexões

**O que mostrar:**
```
"VISUALIZAÇÃO INTERATIVA DO CONFLITO

Cores dos nós:
• Vermelho - Agentes (Prefeitura, Câmara, Comunidade)
• Azul - Ações (Criar PREZEIS, Sancionar Remembramento)
• Amarelo - Normas (Leis, Projetos)
• Verde - Espaços (ZEIS, Centro)
• Laranja - Instrumentos (PEUC, TDC)
• Roxo - Danos (Gentrificação, Caos)
• Verde claro - Benefícios (Moradia, Dignidade)

Arestas mostram relações:
• executaAcao - Quem faz o quê
• conflitaCom - Conflitos normativos
• causa_direta - Cadeias causais
• gera_beneficio - Resultados positivos
"
```

**Demonstração ao vivo:**
1. Clique em "Prefeitura_do_Recife"
   - Mostra que executa múltiplas ações (ambiguidade)
2. Clique em "Lei_do_PREZEIS_1995"
   - Mostra conflito com Lei do Remembramento
3. Clique em "Acao_Sancionar_Lei_Remembramento"
   - Mostra cadeia: Ação → Dano (Gentrificação)

**Ponto técnico chave:**
"Este grafo é gerado automaticamente a partir das triplas RDF. Cada nó e aresta representa conhecimento formal na ontologia."

---

## 🎤 ROTEIRO DE PERGUNTAS E RESPOSTAS

### Pergunta: "Como você garante a consistência do modelo?"

**Resposta (apontando para axioms_diagram.png):**
```
"Através de 3 mecanismos:

1. AXIOMAS DE DISJUNÇÃO (quadrante superior esquerdo)
   • Impedem classificações contraditórias
   • Exemplo: Uma ação não pode ser positiva E negativa

2. RESTRIÇÕES DE DOMÍNIO/RANGE (quadrante inferior direito)
   • Validam automaticamente as relações
   • Exemplo: Apenas ações impeditivas podem causar danos

3. REASONER OWL-RL
   • Verifica todas as restrições
   • Se houver inconsistência, o sistema falha
   • Isso garante que o modelo é logicamente válido
"
```

---

### Pergunta: "Qual a diferença entre isso e um banco de dados relacional?"

**Resposta (apontando para statistics.png):**
```
"Três diferenças fundamentais:

1. INFERÊNCIA AUTOMÁTICA (gráfico de pizza)
   • 70% do conhecimento é INFERIDO
   • Em SQL, você teria que escrever queries para cada inferência
   • Aqui, o reasoner descobre automaticamente

2. RACIOCÍNIO LÓGICO (axioms_diagram.png)
   • Propriedades simétricas: A→B implica B→A
   • Propriedades transitivas: A→B→C implica A→C
   • SQL não tem isso nativamente

3. FLEXIBILIDADE SEMÂNTICA (class_hierarchy.png)
   • Schema aberto, fácil evoluir
   • Adicionar novos conceitos não quebra o modelo
   • Interoperável com outras ontologias (padrão W3C)
"
```

---

### Pergunta: "Como isso pode virar um paper internacional?"

**Resposta (apontando para architecture.png):**
```
"Contribuições originais:

1. MODELAGEM FORMAL DE CONFLITOS URBANOS
   • Primeira ontologia OWL para conflitos legais urbanos
   • Axiomas formais para contradições normativas
   • Replicável em outras cidades

2. DETECÇÃO AUTOMÁTICA DE INCONSISTÊNCIAS
   • Sistema identifica conflitos legais automaticamente
   • Rastreia cadeias de causalidade
   • Mapeia fragmentação institucional

3. APLICAÇÃO PRÁTICA
   • Caso real: PREZEIS vs Remembramento no Recife
   • Ferramenta de auditoria de políticas públicas
   • Base para sistemas de smart cities

4. ÁREAS DE PUBLICAÇÃO
   • Urban Planning & Technology
   • Semantic Web & Ontologies
   • E-Government & Smart Cities
   • Public Policy Analysis

Posso demonstrar cada funcionalidade com consultas SPARQL ao vivo."
```

---

## 📊 DEMONSTRAÇÃO AO VIVO

### Script de Demonstração:

```bash
# 1. Mostrar a pipeline completa
python src/build_knowledge_base.py

# 2. Executar testes
pytest tests/test_ontologia.py -v

# 3. Executar consultas avançadas
python test_queries_advanced.py

# 4. Abrir grafo interativo
# (Abrir visualizations/ontology_interactive.html no navegador)
```

---

## 🎯 CHECKLIST DE APRESENTAÇÃO

Antes de apresentar, certifique-se:

### Arquivos Gerados:
- [ ] `visualizations/architecture.png`
- [ ] `visualizations/class_hierarchy.png`
- [ ] `visualizations/axioms_diagram.png`
- [ ] `visualizations/statistics.png`
- [ ] `visualizations/ontology_interactive.html`

### Demonstrações Funcionando:
- [ ] Pipeline executa sem erros
- [ ] Testes passam (5/5)
- [ ] Consultas avançadas retornam resultados
- [ ] Grafo interativo abre no navegador

### Conhecimento Técnico:
- [ ] Consegue explicar cada axioma
- [ ] Consegue explicar a diferença vs SQL
- [ ] Consegue mostrar inferências no código
- [ ] Consegue executar consultas SPARQL ao vivo

---

## 💡 DICAS FINAIS

1. **Comece pelo architecture.png**
   - Dá visão geral do sistema
   - Mostra as 4 camadas

2. **Use o grafo interativo para "WOW factor"**
   - Deixe o professor explorar
   - Mostre as conexões ao vivo

3. **Enfatize os números**
   - 751 triplas inferidas
   - 3.3x de expansão
   - 0.17 segundos

4. **Conecte com aplicação real**
   - Não é apenas teoria
   - Resolve problema real do Recife
   - Replicável em outras cidades

5. **Mostre código quando perguntarem**
   - Tenha o VS Code aberto
   - Mostre os axiomas no código
   - Execute consultas SPARQL ao vivo

---

**BOA APRESENTAÇÃO! 🚀**
