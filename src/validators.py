# src/validators.py
"""
Módulos de Validação para a Ontologia de Conflitos Urbanos.
"""

from rdflib import Graph, Namespace, RDF, RDFS, OWL
from collections import namedtuple

# Define um tipo de resultado padrão para as validações
ValidationResult = namedtuple('ValidationResult', ['is_valid', 'message', 'details'])

class OntologyValidator:
    """Encapsula lógicas de validação para o schema da ontologia."""

    def __init__(self, graph: Graph):
        """
        Inicializa o validador com um grafo RDFLib.
        
        Args:
            graph (Graph): O grafo do schema a ser validado.
        """
        self.graph = graph
        self.REC = Namespace("http://recife.leg.br/ontologia-conflito#")

    def validate_classes(self, expected_classes: list) -> ValidationResult:
        """Verifica se uma lista de classes esperadas existe no schema."""
        
        found_classes = set()
        missing_classes = []
        
        # Pega todas as classes declaradas no grafo
        declared_classes = {s.split('#')[-1] for s, p, o in self.graph.triples((None, RDF.type, OWL.Class)) if isinstance(s, self.REC)}
        
        for cls_name in expected_classes:
            if cls_name in declared_classes:
                found_classes.add(cls_name)
            else:
                missing_classes.append(cls_name)
        
        is_valid = len(missing_classes) == 0
        message = "Todas as classes esperadas foram encontradas." if is_valid else f"Classes faltando: {', '.join(missing_classes)}"
        
        details = {
            "total_expected": len(expected_classes),
            "total_found": len(found_classes),
            "found_classes": list(found_classes),
            "missing_classes": missing_classes
        }
        
        return ValidationResult(is_valid, message, details)

    def validate_properties(self) -> ValidationResult:
        """Verifica as propriedades de objeto e de dados no schema."""
        
        obj_props = []
        for s in self.graph.subjects(RDF.type, OWL.ObjectProperty):
            if isinstance(s, self.REC):
                domain = self.graph.value(s, RDFS.domain)
                range_ = self.graph.value(s, RDFS.range)
                obj_props.append({
                    "name": s.split('#')[-1],
                    "domain": domain.split('#')[-1] if domain else "N/A",
                    "range": range_.split('#')[-1] if range_ else "N/A"
                })

        is_valid = len(obj_props) > 0
        message = f"Encontradas {len(obj_props)} propriedades de objeto." if is_valid else "Nenhuma propriedade de objeto encontrada."
        details = {
            "total_properties": len(obj_props),
            "object_properties": obj_props
        }
        
        return ValidationResult(is_valid, message, details)

    def validate_disjointness(self) -> ValidationResult:
        """Verifica se restrições 'owl:disjointWith' existem."""
        
        disjoint_pairs = []
        for s, o in self.graph.subject_objects(OWL.disjointWith):
            if isinstance(s, self.REC) and isinstance(o, self.REC):
                pair = tuple(sorted((s.split('#')[-1], o.split('#')[-1])))
                if pair not in disjoint_pairs:
                    disjoint_pairs.append(pair)
        
        is_valid = len(disjoint_pairs) > 0
        message = f"Encontradas {len(disjoint_pairs)} restrições de disjunção." if is_valid else "Nenhuma restrição de disjunção encontrada."
        details = {
            "total_disjoint_constraints": len(disjoint_pairs),
            "disjoint_pairs": disjoint_pairs
        }
        
        return ValidationResult(is_valid, message, details)
