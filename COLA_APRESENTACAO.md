# 📝 COLA PARA APRESENTAÇÃO

## 🔢 NÚMEROS PARA MEMORIZAR

- **40+** classes
- **25+** propriedades
- **20+** axiomas
- **30+** instâncias
- **332** triplas explícitas
- **1083** triplas totais
- **751** triplas inferidas
- **3.3x** taxa de inferência
- **0.17s** tempo de inferência
- **10** consultas SPARQL
- **7** eixos temáticos

---

## 🎯 AXIOMAS (MEMORIZE ESTES 4)

### 1. Disjunção de Ações
```
Acao_Propositiva ⊥ Acao_Impeditiva
"Uma ação não pode ser positiva E negativa"
```

### 2. Propriedade Simétrica
```
conflitaCom(A, B) → conflitaCom(B, A)
"Se A conflita com B, então B conflita com A"
```

### 3. Propriedade Transitiva
```
coincideCom(A,B) ∧ coincideCom(B,C) → coincideCom(A,C)
"Sobreposição através de múltiplas camadas"
```

### 4. Restrição de Domínio
```
causa_direta: domain = Acao_Impeditiva, range = DanoUrbano
"Apenas ações impeditivas causam danos"
```

---

## 🗣️ FRASES-CHAVE

### Sobre Axiomas:
> "Implementei 20+ axiomas formais, incluindo 3 disjunções, 3 propriedades simétricas, 1 transitiva e 15+ restrições de domínio/range."

### Sobre Inferência:
> "O reasoner OWL-RL expande automaticamente 332 para 1083 triplas em 0.17 segundos. 70% do conhecimento é inferido, não inserido manualmente."

### Sobre Diferença vs SQL:
> "SQL armazena dados. Ontologia raciocina sobre dados. Propriedades simétricas e transitivas são automáticas, não preciso escrever queries para cada inferência."

### Sobre Aplicação:
> "O sistema detecta automaticamente conflitos legais, rastreia cadeias de causalidade e mapeia fragmentação institucional. É uma ferramenta de auditoria de políticas públicas."

### Sobre Paper:
> "É a primeira ontologia OWL para conflitos urbanos com axiomas formais. Replicável em outras cidades brasileiras. Aplicável em smart cities e e-government."

---

## 📊 ORDEM DAS VISUALIZAÇÕES

1. **architecture.png** → "4 camadas do sistema"
2. **statistics.png** → "332 → 1083 triplas"
3. **axioms_diagram.png** → "4 axiomas principais"
4. **ontology_interactive.html** → "Grafo ao vivo"
5. **test_queries_advanced.py** → "Consultas funcionando"

---

## ❓ PERGUNTAS PROVÁVEIS

### "Tem axiomas?"
✅ SIM. 20+ axiomas formais.

### "Tem inferência?"
✅ SIM. 751 triplas inferidas (3.3x).

### "Como funciona?"
✅ Reasoner OWL-RL aplica regras lógicas.

### "Diferença vs SQL?"
✅ Raciocínio automático, não apenas armazenamento.

### "Aplicação prática?"
✅ Auditoria de políticas, detecção de conflitos.

### "Potencial de paper?"
✅ Primeira ontologia OWL para conflitos urbanos.

---

## 🎬 DEMONSTRAÇÃO AO VIVO

```bash
# 1. Pipeline
python src/build_knowledge_base.py

# 2. Testes
pytest tests/test_ontologia.py -v

# 3. Consultas
python test_queries_advanced.py

# 4. Visualizações
python visualize_ontology.py
```

---

## 💡 SE TRAVAR

### Não lembra um axioma?
"Posso mostrar no código" → Abra `src/build_knowledge_base.py`

### Não lembra uma consulta?
"Posso executar ao vivo" → Execute `test_queries_advanced.py`

### Pergunta muito técnica?
"Está documentado aqui" → Abra `AXIOMAS_E_INFERENCIAS.md`

---

## ✅ CHECKLIST RÁPIDO

Antes de apresentar:
- [ ] Pipeline executou sem erros?
- [ ] Testes passaram (5/5)?
- [ ] Visualizações geradas?
- [ ] Grafo interativo abre?
- [ ] Números memorizados?
- [ ] Frases-chave decoradas?

---

**RESPIRE FUNDO. VOCÊ SABE DISSO. VOCÊ CONSEGUE! 🚀**
