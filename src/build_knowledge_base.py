# src/build_knowledge_base.py
"""
Script principal da pipeline de construção da Base de Conhecimento (V5).

Execução:
1. Define e salva o Schema V5.
2. Adiciona as instâncias do conflito e salva a base de conhecimento.
3. Executa o reasoner OWL e salva o grafo final inferido.
"""
import time
import os
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL
import owlrl

# --- SETUP DE CAMINHOS ROBUSTOS ---
# Constrói caminhos a partir da localização deste arquivo, para que funcione de qualquer lugar.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True) # Garante que o diretório 'data' exista

# Namespace principal
REC = Namespace("http://recife.leg.br/ontologia-conflito#")

def build_schema():
    """Define e salva o Schema V5 da ontologia."""
    print("--- Passo 1: Definindo o Schema V5 ---")
    g = Graph()
    g.bind("rec", REC)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)

    # CLASSES
    classes = {
        "AgenteUrbano": None, "PoderPublico": "AgenteUrbano", "AgenteExecutivo": "PoderPublico",
        "AgenteLegislativo": "PoderPublico", "Comunidade": "AgenteUrbano", "AcaoUrbana": None,
        "Acao_Propositiva": "AcaoUrbana", "Acao_Impeditiva": "AcaoUrbana", "DanoUrbano": None,
        "BeneficioUrbano": None, "Norma": None, "LegislacaoUrbana": "Norma"
    }
    for name, parent in classes.items():
        cls = REC[name]
        g.add((cls, RDF.type, OWL.Class))
        g.add((cls, RDFS.label, Literal(name.replace('_', ' '))))
        if parent:
            g.add((cls, RDFS.subClassOf, REC[parent]))

    # RESTRIÇÕES
    g.add((REC.Acao_Propositiva, OWL.disjointWith, REC.Acao_Impeditiva))
    g.add((REC.DanoUrbano, OWL.disjointWith, REC.BeneficioUrbano))

    # PROPRIEDADES
    properties = {
        "executaAcao": (OWL.ObjectProperty, {RDFS.domain: REC.AgenteUrbano, RDFS.range: REC.AcaoUrbana}),
        "causa_direta": (OWL.ObjectProperty, {RDFS.domain: REC.Acao_Impeditiva, RDFS.range: REC.DanoUrbano}),
        "gera_beneficio": (OWL.ObjectProperty, {RDFS.domain: REC.Acao_Propositiva, RDFS.range: REC.BeneficioUrbano}),
        "conflitaCom": (OWL.ObjectProperty, {RDFS.domain: REC.Norma, RDFS.range: REC.Norma})
    }
    for name, (prop_type, constraints) in properties.items():
        prop = REC[name]
        g.add((prop, RDF.type, prop_type))
        for constraint, value in constraints.items():
            g.add((prop, constraint, value))
    g.add((REC.conflitaCom, RDF.type, OWL.SymmetricProperty))

    # SALVAR
    output_path = os.path.join(DATA_DIR, "ontologia_conflito_urbano_schema_v5.ttl")
    g.serialize(destination=output_path, format="turtle")
    print(f"✓ Schema V5 salvo em: {output_path}")
    return output_path

def populate_instances(schema_path):
    """Adiciona instâncias ao schema e salva a base de conhecimento."""
    print("\n--- Passo 2: Instanciando o conflito ---")
    g = Graph()
    g.parse(schema_path, format="turtle")

    # INDIVÍDUOS
    instances = {
        "Prefeitura_do_Recife": (REC.AgenteExecutivo, "Prefeitura do Recife"),
        "Camara_Municipal_do_Recife": (REC.AgenteLegislativo, "Câmara Municipal do Recife"),
        "Lei_do_PREZEIS_1995": (REC.LegislacaoUrbana, "Lei do PREZEIS (1995)"),
        "Lei_do_Remembramento_2020": (REC.LegislacaoUrbana, "Lei do Remembramento (2020)"),
        "Acao_Criar_Lei_PREZEIS": (REC.Acao_Propositiva, "Criar Lei do PREZEIS"),
        "Acao_Sancionar_Lei_Remembramento": (REC.Acao_Impeditiva, "Sancionar Lei do Remembramento"),
        "Risco_de_Gentrificacao": (REC.DanoUrbano, "Risco de Gentrificação"),
        "Direito_a_Moradia": (REC.BeneficioUrbano, "Direito à Moradia")
    }
    for name, (type, label) in instances.items():
        inst = REC[name]
        g.add((inst, RDF.type, type))
        g.add((inst, RDFS.label, Literal(label)))

    # RELAÇÕES (NARRATIVA)
    g.add((REC.Camara_Municipal_do_Recife, REC.executaAcao, REC.Acao_Criar_Lei_PREZEIS))
    g.add((REC.Prefeitura_do_Recife, REC.executaAcao, REC.Acao_Sancionar_Lei_Remembramento))
    g.add((REC.Acao_Criar_Lei_PREZEIS, REC.gera_beneficio, REC.Direito_a_Moradia))
    g.add((REC.Acao_Sancionar_Lei_Remembramento, REC.causa_direta, REC.Risco_de_Gentrificacao))
    g.add((REC.Lei_do_PREZEIS_1995, REC.conflitaCom, REC.Lei_do_Remembramento_2020))

    # SALVAR
    output_path = os.path.join(DATA_DIR, "kb_conflito_v5_final.ttl")
    g.serialize(destination=output_path, format="turtle")
    print(f"✓ Grafo com instâncias salvo em: {output_path}")
    return output_path

def run_inference(kb_path):
    """Executa o reasoner OWL e salva o grafo inferido."""
    print("\n--- Passo 3: Executando o Reasoner OWL DL ---")
    g = Graph()
    g.parse(kb_path, format="turtle")
    triplas_antes = len(g)
    print(f"Triplas antes da inferência: {triplas_antes}")

    start_time = time.time()
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    elapsed_time = time.time() - start_time

    triplas_depois = len(g)
    print(f"Triplas depois da inferência: {triplas_depois}")
    print(f"Novas triplas inferidas: {triplas_depois - triplas_antes}")
    print(f"Inferência concluída em {elapsed_time:.3f} segundos.")

    # SALVAR
    output_path = os.path.join(DATA_DIR, "kb_conflito_v5_inferido.ttl")
    g.serialize(destination=output_path, format="turtle")
    print(f"✓ Grafo inferido salvo em: {output_path}")
    return output_path

def main():
    """Executa a pipeline completa."""
    schema_file = build_schema()
    kb_file = populate_instances(schema_file)
    run_inference(kb_file)
    print("\nPipeline de construção da base de conhecimento concluída com sucesso!")

if __name__ == "__main__":
    main()
