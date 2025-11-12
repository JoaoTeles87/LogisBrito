# src/sparql_queries.py
"""
Motor de Consultas SPARQL para a Ontologia de Conflitos Urbanos.
"""

class SPARQLQueryEngine:
    """Encapsula a lógica para executar consultas SPARQL predefinidas."""

    def __init__(self, graph):
        """
        Inicializa o motor com um grafo RDFLib.
        
        Args:
            graph (rdflib.Graph): O grafo (preferencialmente inferido) a ser consultado.
        """
        self.graph = graph
        self.namespace_prefix = "PREFIX rec: <http://recife.leg.br/ontologia-conflito#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"

    def _execute_query(self, query):
        """Método auxiliar para executar uma consulta e retornar uma lista de dicionários."""
        full_query = f"{self.namespace_prefix}\n{query}"
        results = self.graph.query(full_query)
        return [row.asdict() for row in results]

    def query_normative_conflict(self):
        """
        (V5) Encontra normas que estão em conflito explícito umas com as outras
        usando a propriedade 'conflitaCom'.
        """
        query = """
            SELECT ?norma1_label ?norma2_label
            WHERE {
                ?norma1 a rec:Norma ;
                        rec:conflitaCom ?norma2 ;
                        rdfs:label ?norma1_label .
                ?norma2 rdfs:label ?norma2_label .
                FILTER(STR(?norma1) < STR(?norma2))
            }
        """
        return self._execute_query(query)

    def query_ambiguous_actors(self):
        """
        Encontra agentes que executam tanto ações propositivas quanto impeditivas.
        """
        query = """
            SELECT DISTINCT ?ator_label ?acao_propositiva_label ?acao_impeditiva_label
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
        return self._execute_query(query)

    def query_causality_chain(self, dano_uri=None):
        """
        Rastreia a cadeia de causalidade de um dano.
        """
        filter_clause = f"FILTER(?dano = <{dano_uri}>)" if dano_uri else ""
        
        query = f"""
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
        return self._execute_query(query)

# Adiciona uma nova linha no final para garantir que o arquivo seja terminado corretamente.