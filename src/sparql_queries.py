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
    
    def query_spatial_overlap(self):
        """
        Detecta sobreposição de zonas legais (explora propriedade transitiva).
        Encontra espaços que coincidem através de múltiplas camadas.
        """
        query = """
            SELECT DISTINCT ?espaco1_label ?espaco2_label
            WHERE {
                ?espaco1 rec:coincideCom ?espaco2 ;
                         rdfs:label ?espaco1_label .
                ?espaco2 rdfs:label ?espaco2_label .
                FILTER(STR(?espaco1) < STR(?espaco2))
            }
        """
        return self._execute_query(query)
    
    def query_legal_breaches(self):
        """
        Identifica "brechas legais" - normas que permitem ações impeditivas.
        Esta é a consulta que revela contradições no sistema legal.
        """
        query = """
            SELECT ?norma_label ?acao_label ?dano_label
            WHERE {
                ?norma rec:permiteExcecao ?acao ;
                       rdfs:label ?norma_label .
                
                ?acao a rec:Acao_Impeditiva ;
                      rec:causa_direta ?dano ;
                      rdfs:label ?acao_label .
                
                ?dano rdfs:label ?dano_label .
            }
        """
        return self._execute_query(query)
    
    def query_institutional_fragmentation(self):
        """
        Mapeia a fragmentação institucional do poder público.
        Mostra quantas agências diferentes existem e suas atribuições.
        """
        query = """
            SELECT ?agencia_label ?tipo ?atribuicao
            WHERE {
                ?agencia a rec:PoderPublico ;
                         rdfs:label ?agencia_label .
                
                ?agencia a ?tipo .
                FILTER(?tipo != <http://www.w3.org/2002/07/owl#Thing>)
                FILTER(?tipo != rec:PoderPublico)
                FILTER(?tipo != rec:AgenteUrbano)
                
                OPTIONAL {
                    ?agencia rec:temAtribuicaoLegal ?atribuicao .
                }
            }
            ORDER BY ?tipo
        """
        return self._execute_query(query)
    
    def query_benefit_damage_reversals(self):
        """
        Encontra pares de benefício-dano onde o benefício reverte o dano.
        Demonstra a lógica de "solução" do sistema.
        """
        query = """
            SELECT ?beneficio_label ?dano_label ?acao_positiva_label ?acao_negativa_label
            WHERE {
                ?beneficio rec:e_reversao_de ?dano ;
                           rdfs:label ?beneficio_label .
                
                ?dano rdfs:label ?dano_label .
                
                ?acao_positiva rec:gera_beneficio ?beneficio ;
                               rdfs:label ?acao_positiva_label .
                
                ?acao_negativa rec:causa_direta ?dano ;
                               rdfs:label ?acao_negativa_label .
            }
        """
        return self._execute_query(query)
    
    def query_market_pressure_on_zeis(self):
        """
        Identifica ZEIS sob pressão imobiliária e os agentes responsáveis.
        Consulta específica para análise de gentrificação.
        """
        query = """
            SELECT ?zeis_label ?agente_mercado_label ?permite_remembramento
            WHERE {
                ?zeis a rec:ZEIS ;
                      rdfs:label ?zeis_label .
                
                OPTIONAL {
                    ?zeis rec:estaSobPressaoImobiliaria ?agente_mercado .
                    ?agente_mercado rdfs:label ?agente_mercado_label .
                }
                
                OPTIONAL {
                    ?zeis rec:permiteRemembramento ?permite_remembramento .
                }
            }
        """
        return self._execute_query(query)
    
    def query_conflicting_jurisdictions(self):
        """
        Detecta conflitos de jurisdição - quando múltiplos órgãos têm tutela
        sobre o mesmo espaço (através de sobreposição espacial).
        """
        query = """
            SELECT ?orgao1_label ?orgao2_label ?espaco_label
            WHERE {
                ?orgao1 rec:exerceTutelaSobre ?espaco1 ;
                        rdfs:label ?orgao1_label .
                
                ?orgao2 rec:exerceTutelaSobre ?espaco2 ;
                        rdfs:label ?orgao2_label .
                
                ?espaco1 rec:coincideCom ?espaco2 ;
                         rdfs:label ?espaco_label .
                
                FILTER(?orgao1 != ?orgao2)
                FILTER(STR(?orgao1) < STR(?orgao2))
            }
        """
        return self._execute_query(query)
    
    def query_full_conflict_narrative(self):
        """
        CONSULTA MESTRE: Reconstrói a narrativa completa do conflito.
        Conecta: Agentes → Ações → Instrumentos → Normas → Danos/Benefícios
        """
        query = """
            SELECT ?agente_label ?acao_label ?instrumento_label 
                   ?norma_label ?resultado_label ?tipo_resultado
            WHERE {
                ?agente rec:executaAcao ?acao ;
                        rdfs:label ?agente_label .
                
                ?acao rdfs:label ?acao_label .
                
                OPTIONAL {
                    ?acao rec:utilizaInstrumento ?instrumento .
                    ?instrumento rdfs:label ?instrumento_label .
                }
                
                OPTIONAL {
                    ?norma rec:institui ?instrumento ;
                           rdfs:label ?norma_label .
                }
                
                {
                    ?acao rec:causa_direta ?resultado .
                    ?resultado rdfs:label ?resultado_label .
                    BIND("DANO" AS ?tipo_resultado)
                }
                UNION
                {
                    ?acao rec:gera_beneficio ?resultado .
                    ?resultado rdfs:label ?resultado_label .
                    BIND("BENEFÍCIO" AS ?tipo_resultado)
                }
            }
            ORDER BY ?agente_label ?tipo_resultado
        """
        return self._execute_query(query)
