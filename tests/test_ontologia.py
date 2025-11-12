# tests/test_ontologia.py
import pytest
import os
from rdflib import Graph, Namespace, RDF, RDFS
import subprocess

# Adiciona o diretório raiz ao path para encontrar os módulos em src
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.build_knowledge_base import BASE_DIR
from src.sparql_queries import SPARQLQueryEngine

REC = Namespace("http://recife.leg.br/ontologia-conflito#")

@pytest.fixture(scope="module")
def inferred_graph():
    """
    Executa a pipeline de build e carrega o grafo final inferido para os testes.
    """
    # Caminhos relativos ao projeto atual (D:\Projetos\LogisBrito) e ao repositório de dados (D:\Projetos\LogisBritodata)
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # D:\Projetos\LogisBrito

    # Arquivo TTL esperado em D:\Projetos\LogisBritodata\kb_conflito_v5_inferido.ttl
    inferred_kb_path = os.path.join(BASE_DIR, 'data', 'kb_conflito_v5_inferido.ttl')

    # Use o mesmo interpretador Python que está executando os testes
    python_executable = sys.executable

   

    # Passo 2: Carregar o grafo gerado
    g = Graph()
    try:
        g.parse(inferred_kb_path, format="turtle")
    except FileNotFoundError:
        pytest.fail(f"O script de build não gerou o arquivo esperado: {inferred_kb_path}")
    
    return g

class TestV5Pipeline:
    """Testa a pipeline completa da V5, validando o grafo gerado pelo script de build."""

    def test_schema_classes_present(self, inferred_graph):
        """Valida se as classes V5 essenciais estão no grafo."""
        expected_classes = [
            REC.AgenteExecutivo, REC.AgenteLegislativo, REC.Norma, REC.LegislacaoUrbana,
            REC.AcaoUrbana, REC.DanoUrbano, REC.BeneficioUrbano
        ]
        for cls in expected_classes:
            assert (cls, RDF.type, RDFS.Class) or (cls, RDF.type, OWL.Class) in inferred_graph, f"A classe {cls} não foi encontrada."

    def test_instance_typing(self, inferred_graph):
        """Valida a tipagem V5 das instâncias."""
        assert (REC.Prefeitura_do_Recife, RDF.type, REC.AgenteExecutivo) in inferred_graph
        assert (REC.Lei_do_PREZEIS_1995, RDF.type, REC.LegislacaoUrbana) in inferred_graph

    def test_inference_of_superclasses(self, inferred_graph):
        """Valida se o reasoner inferiu as superclasses (ex: AgenteExecutivo -> AgenteUrbano)."""
        assert (REC.Prefeitura_do_Recife, RDF.type, REC.AgenteUrbano) in inferred_graph

    def test_sparql_normative_conflict(self, inferred_graph):
        """TESTE CRÍTICO: Valida se a consulta SPARQL encontra o conflito normativo."""
        engine = SPARQLQueryEngine(inferred_graph)
        results = engine.query_normative_conflict()
        
        assert len(results) > 0, "A consulta de conflito normativo não retornou resultados."
        
        first_result = results[0]
        # Converte os literais para string antes da asserção
        labels = {str(first_result['norma1_label']), str(first_result['norma2_label'])}
        
        assert "Lei do PREZEIS (1995)" in labels
        assert "Lei do Remembramento (2020)" in labels

    def test_sparql_causality_chain(self, inferred_graph):
        """Valida a consulta de cadeia de causalidade."""
        engine = SPARQLQueryEngine(inferred_graph)
        results = engine.query_causality_chain()

        assert len(results) > 0, "A consulta de causalidade não retornou resultados."
        
        # Converte os literais para string antes da comparação
        found_chain = any(
            str(res['acao_label']) == 'Sancionar Lei do Remembramento' and 
            str(res['dano_label']) == 'Risco de Gentrificação' 
            for res in results
        )
        assert found_chain, "A cadeia causal esperada (Remembramento -> Gentrificação) não foi encontrada."
