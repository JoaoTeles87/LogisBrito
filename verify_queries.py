"""
Script para verificar os resultados das consultas SPARQL.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from rdflib import Graph, Namespace
from src.sparql_queries import SPARQLQueryEngine

# Carregar o grafo inferido
g = Graph()
g.parse("data/kb_conflito_urbano_inferido.ttl", format="turtle")

# Criar engine de consultas
engine = SPARQLQueryEngine(g)

print("=" * 70)
print("VERIFICAÇÃO DOS RESULTADOS DAS CONSULTAS SPARQL")
print("=" * 70)

# Consulta 1: Atores Ambíguos
print("\n1. CONSULTA DE ATORES AMBÍGUOS")
print("-" * 70)
results_ambiguous = engine.query_ambiguous_actors()
print(f"Resultados encontrados: {len(results_ambiguous)}")

if len(results_ambiguous) > 0:
    for r in results_ambiguous:
        print(f"  ✓ Ator: {r['ator_label']}")
        print(f"    - Ação Propositiva: {r['acao_propositiva_label']}")
        print(f"    - Ação Impeditiva: {r['acao_impeditiva_label']}")
    
    # Verificar se Prefeitura está nos resultados
    ator_labels = [r['ator_label'] for r in results_ambiguous]
    if any('Prefeitura' in label for label in ator_labels):
        print("\n  ✓ SUCESSO: Prefeitura identificada como ator ambíguo")
    else:
        print("\n  ✗ AVISO: Prefeitura não identificada como ator ambíguo")
else:
    print("  ⚠ Nenhum ator ambíguo encontrado")

# Consulta 2: Causalidade
print("\n2. CONSULTA DE CAUSALIDADE (Gentrificação no Coque)")
print("-" * 70)
dano_coque = "http://recife.leg.br/ontologia-conflito#Risco_de_Gentrificacao_Coque"
results_causality = engine.query_causality_chain(dano_coque)
print(f"Resultados encontrados: {len(results_causality)}")

if len(results_causality) > 0:
    for r in results_causality:
        print(f"  ✓ Agente: {r['agente_label']}")
        print(f"    → Ação: {r['acao_label']}")
        print(f"    → Dano: {r['dano_label']}")
    
    # Verificar se rastreia gentrificação no Coque
    dano_labels = [r['dano_label'] for r in results_causality]
    if any('Coque' in label or 'Gentrificação' in label for label in dano_labels):
        print("\n  ✓ SUCESSO: Causalidade de gentrificação no Coque rastreada")
    else:
        print("\n  ✗ AVISO: Gentrificação no Coque não rastreada")
else:
    print("  ⚠ Nenhuma cadeia de causalidade encontrada")

# Consulta 3: Conflito de Instrumentos
print("\n3. CONSULTA DE CONFLITO DE INSTRUMENTOS")
print("-" * 70)
results_conflict = engine.query_conflicting_instruments()
print(f"Resultados encontrados: {len(results_conflict)}")

if len(results_conflict) > 0:
    for r in results_conflict:
        print(f"  ✓ Dano: {r['dano_label']}")
        print(f"    + Ação que reverte: {r['acao_positiva_label']}")
        print(f"    - Ação que causa: {r['acao_negativa_label']}")
    
    # Verificar se identifica conflito PREZEIS vs Remembramento
    acao_positiva_labels = [r['acao_positiva_label'] for r in results_conflict]
    acao_negativa_labels = [r['acao_negativa_label'] for r in results_conflict]
    
    prezeis_found = any('PREZEIS' in label for label in acao_positiva_labels)
    remembramento_found = any('Remembramento' in label or 'Lei 18772' in label or 'Sancionar' in label 
                              for label in acao_negativa_labels)
    
    if prezeis_found and remembramento_found:
        print("\n  ✓ SUCESSO: Conflito PREZEIS vs Remembramento identificado")
    else:
        print(f"\n  ✗ AVISO: Conflito não totalmente identificado")
        print(f"    PREZEIS encontrado: {prezeis_found}")
        print(f"    Remembramento encontrado: {remembramento_found}")
else:
    print("  ⚠ Nenhum conflito de instrumentos encontrado")

print("\n" + "=" * 70)
print("VERIFICAÇÃO CONCLUÍDA")
print("=" * 70)
