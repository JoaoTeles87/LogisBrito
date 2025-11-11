"""
Módulo para consultas SPARQL reutilizáveis sobre a ontologia de conflitos urbanos.
"""

from typing import List, Dict
from rdflib import Graph


class SPARQLQueryEngine:
    """Motor de consultas SPARQL para análise de conflitos urbanos."""
    
    def __init__(self, graph: Graph):
        """
        Inicializa o motor de consultas com um grafo RDF.
        
        Args:
            graph: Grafo RDF contendo a ontologia e instâncias
        """
        self.graph = graph
        self.namespace_prefix = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rec: <http://recife.leg.br/ontologia-conflito#>
        """
    
    def query_ambiguous_actors(self) -> List[Dict[str, str]]:
        """
        Identifica atores executando ações de classes opostas (Propositiva e Impeditiva).
        
        Esta consulta revela a ambiguidade do Poder Público, que simultaneamente
        propõe instrumentos de proteção e sanciona instrumentos que causam danos.
        
        Returns:
            Lista de dicionários com chaves: ator_label, acao_propositiva_label, acao_impeditiva_label
        """
        query = self.namespace_prefix + """
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
        """
        
        results = []
        for row in self.graph.query(query):
            results.append({
                'ator_label': str(row.ator_label),
                'acao_propositiva_label': str(row.acao_propositiva_label),
                'acao_impeditiva_label': str(row.acao_impeditiva_label)
            })
        return results
    
    def query_causality_chain(self, dano_uri: str = None) -> List[Dict[str, str]]:
        """
        Rastreia a cadeia de causalidade de danos urbanos.
        
        Identifica quais agentes executam ações que causam danos específicos,
        revelando a responsabilidade por processos como gentrificação.
        
        Args:
            dano_uri: URI do dano específico (opcional). Se None, retorna todos os danos.
        
        Returns:
            Lista de dicionários com chaves: agente_label, acao_label, dano_label
        """
        filter_clause = f"FILTER(?dano = <{dano_uri}>)" if dano_uri else ""
        
        query = self.namespace_prefix + f"""
            SELECT ?agente_label ?acao_label ?dano_label
            WHERE {{
                ?acao a rec:Acao_Impeditiva ;
                      rec:causa_direta ?dano ;
                      rdfs:label ?acao_label .
                ?agente rec:executaAcao ?acao ;
                        rdfs:label ?agente_label .
                ?dano rdfs:label ?dano_label .
                {filter_clause}
            }}
        """
        
        results = []
        for row in self.graph.query(query):
            results.append({
                'agente_label': str(row.agente_label),
                'acao_label': str(row.acao_label),
                'dano_label': str(row.dano_label)
            })
        return results
    
    def query_conflicting_instruments(self) -> List[Dict[str, str]]:
        """
        Identifica instrumentos em conflito direto sobre o mesmo dano.
        
        Revela situações onde uma ação propositiva tenta reverter um dano
        que é simultaneamente causado por uma ação impeditiva, evidenciando
        conflitos lógicos na política urbana.
        
        Returns:
            Lista de dicionários com chaves: dano_label, acao_positiva_label, acao_negativa_label
        """
        query = self.namespace_prefix + """
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
        """
        
        results = []
        for row in self.graph.query(query):
            results.append({
                'dano_label': str(row.dano_label),
                'acao_positiva_label': str(row.acao_positiva_label),
                'acao_negativa_label': str(row.acao_negativa_label)
            })
        return results
    
    def format_results(self, results: List[Dict[str, str]], query_type: str) -> str:
        """
        Formata resultados de consultas SPARQL para exibição legível.
        
        Args:
            results: Lista de dicionários retornada por uma consulta
            query_type: Tipo da consulta ('ambiguous_actors', 'causality_chain', 'conflicting_instruments')
        
        Returns:
            String formatada com os resultados
        """
        if not results:
            return "Nenhum resultado encontrado."
        
        output = []
        
        if query_type == 'ambiguous_actors':
            output.append("=" * 80)
            output.append("ATORES AMBÍGUOS - Executando Ações Opostas")
            output.append("=" * 80)
            for i, result in enumerate(results, 1):
                output.append(f"\n{i}. Ator: {result['ator_label']}")
                output.append(f"   ├─ Ação Propositiva: {result['acao_propositiva_label']}")
                output.append(f"   └─ Ação Impeditiva: {result['acao_impeditiva_label']}")
                output.append(f"   ⚠️  CONFLITO: O mesmo ator executa ações de classes disjuntas!")
        
        elif query_type == 'causality_chain':
            output.append("=" * 80)
            output.append("CADEIA DE CAUSALIDADE - Danos Urbanos")
            output.append("=" * 80)
            for i, result in enumerate(results, 1):
                output.append(f"\n{i}. Agente: {result['agente_label']}")
                output.append(f"   ├─ Executa: {result['acao_label']}")
                output.append(f"   └─ Causa: {result['dano_label']}")
        
        elif query_type == 'conflicting_instruments':
            output.append("=" * 80)
            output.append("CONFLITO DE INSTRUMENTOS - Sobre o Mesmo Dano")
            output.append("=" * 80)
            for i, result in enumerate(results, 1):
                output.append(f"\n{i}. Dano: {result['dano_label']}")
                output.append(f"   ├─ Instrumento Protetor: {result['acao_positiva_label']}")
                output.append(f"   └─ Instrumento Causador: {result['acao_negativa_label']}")
                output.append(f"   ⚠️  CONFLITO LÓGICO: Instrumentos opostos sobre o mesmo dano!")
        
        output.append("\n" + "=" * 80)
        output.append(f"Total de resultados: {len(results)}")
        output.append("=" * 80)
        
        return "\n".join(output)
