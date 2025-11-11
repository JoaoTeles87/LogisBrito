# Resultados da Análise - LogisBrito

Este documento apresenta os resultados obtidos pela aplicação da ontologia LogisBrito ao caso do conflito urbano do Coque, em Recife.

---

## Triplas Inferidas pelo Reasoner

O reasoner OWL DL (`owlrl`) deduziu automaticamente novos fatos a partir das regras definidas no schema da ontologia.

### Estatísticas de Inferência

| Métrica | Valor |
|---------|-------|
| Triplas antes da inferência | 78 |
| Triplas depois da inferência | 95+ |
| Triplas inferidas | 17+ |
| Tempo de execução | < 1 segundo |

### Principais Triplas Inferidas

#### 1. Inferência de Superclasses

**Regra OWL:** Se `X` é instância de `Y` e `Y` é subclasse de `Z`, então `X` é instância de `Z`.

**Exemplos:**

```turtle
# Declarado explicitamente:
rec:Prefeitura_do_Recife a rec:PoderPublico .

# Inferido automaticamente:
rec:Prefeitura_do_Recife a rec:AgenteUrbano .
```

**Justificativa:** `PoderPublico` é subclasse de `AgenteUrbano`, portanto a Prefeitura herda essa tipagem.

---

```turtle
# Declarado explicitamente:
rec:Comunidade_do_Coque a rec:Comunidade .

# Inferido automaticamente:
rec:Comunidade_do_Coque a rec:AgenteUrbano .
```

**Justificativa:** `Comunidade` é subclasse de `AgenteUrbano`.

---

```turtle
# Declarado explicitamente:
rec:Agentes_Especulativos_da_Orla a rec:Agente_Especulativo .

# Inferido automaticamente:
rec:Agentes_Especulativos_da_Orla a rec:Agente_de_Mercado .
rec:Agentes_Especulativos_da_Orla a rec:AgenteUrbano .
```

**Justificativa:** `Agente_Especulativo` ⊆ `Agente_de_Mercado` ⊆ `AgenteUrbano`.

---

#### 2. Inferência de Tipagem por Domain/Range

**Regra OWL:** Se propriedade `P` tem domain `D` e `X P Y`, então `X` é instância de `D`.

**Exemplos:**

```turtle
# Declarado explicitamente:
rec:Acao_Propor_Lei_PREZEIS_1995 rec:reverte_por_forca rec:Risco_de_Gentrificacao_Coque .

# Inferido automaticamente:
rec:Acao_Propor_Lei_PREZEIS_1995 a rec:Acao_Propositiva .
```

**Justificativa:** `reverte_por_forca` tem domain `Acao_Propositiva`.

---

#### 3. Inferência de Simetria

**Regra OWL:** Se propriedade `P` é simétrica e `X P Y`, então `Y P X`.

**Exemplo:**

```turtle
# Declarado explicitamente:
rec:Agentes_Especulativos_da_Orla rec:em_antagonismo_com rec:Comunidade_do_Coque .

# Inferido automaticamente:
rec:Comunidade_do_Coque rec:em_antagonismo_com rec:Agentes_Especulativos_da_Orla .
```

**Justificativa:** `em_antagonismo_com` é declarada como `owl:SymmetricProperty`.

---

### Importância da Inferência

A inferência automática permite:

1. **Reduzir Redundância:** Não é necessário declarar explicitamente que a Prefeitura é `AgenteUrbano` — o reasoner deduz isso.
2. **Garantir Consistência:** Se uma instância violar restrições (ex: ser membro de classes disjuntas), o reasoner detecta a inconsistência.
3. **Facilitar Consultas:** Consultas SPARQL podem buscar por `AgenteUrbano` e encontrar automaticamente todas as subclasses (PoderPublico, Comunidade, etc.).

---

## Narrativas Extraídas pelas Consultas SPARQL

As consultas SPARQL extraem padrões específicos do grafo inferido, revelando narrativas de conflito.

### Consulta 1: Atores Ambíguos

**Objetivo:** Identificar agentes que executam ações de classes opostas (propositiva E impeditiva).

#### Resultados

| Ator | Ação Propositiva | Ação Impeditiva |
|------|------------------|-----------------|
| **Prefeitura do Recife** | Propor Lei PREZEIS 1995 | Sancionar Lei do Remembramento 2020 |
| **Prefeitura do Recife** | Propor Lei PREZEIS 1995 | Omitir Fiscalização PREZEIS |

#### Interpretação

A Prefeitura do Recife age de forma **contraditória**:

- **Ação Propositiva:** Criou a Lei PREZEIS em 1995 para proteger ZEIS como o Coque.
- **Ações Impeditivas:**
  - Sancionou a Lei do Remembramento (2020), que facilita a unificação de lotes e gentrificação.
  - Omitiu fiscalização da PREZEIS, permitindo ocupação irregular.

**Conclusão:** O poder público apresenta **ambiguidade comportamental**, protegendo e ameaçando simultaneamente a mesma comunidade.

---

### Consulta 2: Causalidade de Danos

**Objetivo:** Rastrear a cadeia de causalidade de danos urbanos.

#### Resultados

| Agente | Ação | Dano Causado |
|--------|------|--------------|
| **Prefeitura do Recife** | Sancionar Lei do Remembramento 2020 | Risco de Gentrificação Coque |
| **Prefeitura do Recife** | Omitir Fiscalização PREZEIS | Risco de Gentrificação Coque |
| **Agentes Especulativos da Orla** | Sancionar Lei do Remembramento 2020 | Risco de Gentrificação Coque |

#### Interpretação

O **Risco de Gentrificação do Coque** é causado por três ações impeditivas:

1. **Lei do Remembramento (2020):** Permite unificação de lotes, facilitando especulação imobiliária.
2. **Omissão de Fiscalização:** Permite ocupação irregular e enfraquece proteção da ZEIS.
3. **Pressão Especulativa:** Agentes de mercado exploram brechas legais.

**Conclusão:** A gentrificação não é um fenômeno "natural", mas resultado de **ações concretas e identificáveis** de agentes específicos.

---

### Consulta 3: Conflito de Instrumentos

**Objetivo:** Identificar instrumentos legais em conflito direto sobre o mesmo dano.

#### Resultados

| Dano | Instrumento Protetor | Instrumento Agressor |
|------|---------------------|---------------------|
| **Risco de Gentrificação Coque** | Lei PREZEIS 1995 (Ação Propositiva) | Lei do Remembramento 2020 (Ação Impeditiva) |

#### Interpretação

Duas leis municipais atuam em **direções opostas**:

- **Lei PREZEIS (1995):** Protege ZEIS, garantindo permanência de comunidades de baixa renda.
- **Lei do Remembramento (2020):** Facilita unificação de lotes, incentivando especulação e gentrificação.

**Conclusão:** Há uma **contradição legislativa** no sistema legal de Recife. A Lei do Remembramento enfraquece a proteção estabelecida pela PREZEIS.

---

## Análise dos Conflitos Identificados

### Conflito 1: Ambiguidade do Poder Público

**Natureza:** Incoerência política.

**Evidência:** A Prefeitura executa ações propositivas (PREZEIS) e impeditivas (Remembramento, omissão).

**Implicações:**
- Questiona a legitimidade das ações do poder público.
- Sugere captura do Estado por interesses especulativos.
- Permite argumentação jurídica sobre má-fé administrativa.

**Possíveis Causas:**
- Mudança de gestão política (diferentes prefeitos).
- Pressão de lobbies imobiliários.
- Falta de coordenação entre secretarias municipais.

---

### Conflito 2: Contradição Legislativa

**Natureza:** Inconsistência normativa.

**Evidência:** PREZEIS e Remembramento regulam o mesmo território de forma oposta.

**Implicações:**
- Cria insegurança jurídica para moradores e investidores.
- Permite interpretações seletivas da lei.
- Enfraquece proteção de ZEIS.

**Possíveis Soluções:**
- Revogar Lei do Remembramento.
- Criar exceção explícita para ZEIS.
- Harmonizar legislação urbanística.

---

### Conflito 3: Causalidade Compartilhada

**Natureza:** Responsabilidade difusa.

**Evidência:** Múltiplos agentes causam o mesmo dano (gentrificação).

**Implicações:**
- Dificulta atribuição de responsabilidade.
- Permite que cada ator negue culpa individual.
- Requer ação coordenada para reverter dano.

**Estratégia de Advocacy:**
- Mapear cadeia causal completa.
- Identificar pontos de intervenção.
- Propor ações específicas para cada agente.

---

## Como o Sistema Detecta Ambiguidade do Poder Público

O sistema detecta ambiguidade através de um padrão lógico específico na consulta SPARQL:

### Padrão de Detecção

```sparql
SELECT ?ator ?acao_propositiva ?acao_impeditiva
WHERE {
    ?ator a rec:AgenteUrbano ;
          rec:executaAcao ?acao_propositiva ;
          rec:executaAcao ?acao_impeditiva .
    
    ?acao_propositiva a rec:Acao_Propositiva .
    ?acao_impeditiva a rec:Acao_Impeditiva .
}
```

### Lógica de Detecção

1. **Busca Agentes:** Identifica todos os `AgenteUrbano`.
2. **Busca Ações:** Para cada agente, busca ações executadas via `executaAcao`.
3. **Filtra por Tipo:** Separa ações em propositivas e impeditivas.
4. **Detecta Contradição:** Se o mesmo agente executa ambos os tipos, há ambiguidade.

### Por que Isso é Ambiguidade?

- **Classes Disjuntas:** `Acao_Propositiva` e `Acao_Impeditiva` são declaradas como `owl:disjointWith`.
- **Semântica Oposta:** Ações propositivas geram benefícios; impeditivas causam danos.
- **Incoerência Comportamental:** Um agente não deveria simultaneamente proteger e ameaçar o mesmo bem.

### Diferença de Inconsistência Lógica

**Importante:** A Prefeitura não é **logicamente inconsistente** (não viola restrições OWL). Ela é **comportamentalmente ambígua** (executa ações contraditórias).

- **Inconsistência Lógica:** Instância declarada como membro de classes disjuntas (ex: `X a Acao_Propositiva, Acao_Impeditiva`).
- **Ambiguidade Comportamental:** Instância executa ações de classes disjuntas (ex: `Prefeitura executaAcao A1, A2` onde `A1` é propositiva e `A2` é impeditiva).

O reasoner não detecta ambiguidade automaticamente — ela é identificada pela **consulta SPARQL customizada**.

---

## Validação dos Resultados

### Testes Automatizados

Todos os resultados foram validados por testes pytest:

```bash
pytest tests/test_ontologia.py -v
```

**Resultados:**
- ✓ Schema carregado sem erros
- ✓ Classes principais presentes
- ✓ Propriedades com domain/range corretos
- ✓ Restrições disjointWith presentes
- ✓ Instâncias corretamente tipadas
- ✓ Inferência de subclasses funcionando
- ✓ Consultas SPARQL retornando resultados esperados

### Verificação Manual

Os resultados foram verificados manualmente:

1. **Consulta de Atores Ambíguos:** Confirmado que Prefeitura aparece nos resultados.
2. **Consulta de Causalidade:** Confirmado que três ações causam gentrificação.
3. **Consulta de Conflito:** Confirmado que PREZEIS e Remembramento estão em conflito.

---

## Limitações e Trabalhos Futuros

### Limitações Atuais

1. **Escopo Limitado:** Apenas um caso (Coque) modelado.
2. **Dados Simplificados:** Instâncias não incluem datas, valores monetários, etc.
3. **Sem Dados Geoespaciais:** Não há integração com shapefiles ou coordenadas.
4. **Sem Interface Web:** Consultas requerem conhecimento de Python/SPARQL.

### Próximos Passos

1. **Expandir Base de Conhecimento:**
   - Adicionar outros casos (Brasília Teimosa, Cais José Estelita).
   - Modelar mais instrumentos (Estatuto da Cidade, Plano Diretor).

2. **Enriquecer Dados:**
   - Adicionar propriedades temporais (datas de sanção de leis).
   - Adicionar propriedades quantitativas (número de famílias afetadas).

3. **Integrar Dados Geoespaciais:**
   - Conectar instâncias de ZEIS com shapefiles.
   - Visualizar conflitos em mapa interativo.

4. **Desenvolver Interface Web:**
   - Criar aplicação Flask/Django para consultas interativas.
   - Permitir upload de novos casos por usuários.

5. **Validar com Especialistas:**
   - Apresentar resultados para urbanistas e juristas.
   - Refinar ontologia com feedback de domínio.

---

## Conclusão

O sistema LogisBrito demonstrou capacidade de:

1. **Inferir Novos Fatos:** Reasoner deduziu 17+ triplas automaticamente.
2. **Detectar Ambiguidade:** Identificou contradição comportamental da Prefeitura.
3. **Rastrear Causalidade:** Mapeou cadeia de responsabilidade pela gentrificação.
4. **Identificar Conflitos Legais:** Revelou contradição entre PREZEIS e Remembramento.

Esses resultados validam a abordagem de **lógica simbólica** para análise de conflitos urbanos, oferecendo uma alternativa auditável e verificável a modelos probabilísticos (LLMs).

O próximo passo é expandir a base de conhecimento e desenvolver ferramentas de visualização para tornar o sistema acessível a não-programadores.
