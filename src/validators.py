"""
Módulo para validação de ontologias OWL DL.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from rdflib import Graph, Namespace, RDF, RDFS, OWL


@dataclass
class ValidationResult:
    """Resultado de uma validação de ontologia."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict = field(default_factory=dict)
    
    def add_error(self, message: str):
        """Adiciona um erro ao resultado."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Adiciona um aviso ao resultado."""
        self.warnings.append(message)


class OntologyValidator:
    """Validador de ontologias OWL DL."""
    
    def __init__(self, graph: Graph):
        """
        Inicializa o validador com um grafo RDF.
        
        Args:
            graph: Grafo RDF contendo a ontologia
        """
        self.graph = graph
        self.rec = Namespace("http://recife.leg.br/ontologia-conflito#")
    
    def validate_syntax(self) -> ValidationResult:
        """
        Valida a sintaxe Turtle do grafo.
        
        Se o grafo foi carregado com sucesso, a sintaxe é válida.
        
        Returns:
            ValidationResult indicando se a sintaxe é válida
        """
        result = ValidationResult(is_valid=True)
        
        try:
            # Se o grafo existe e tem triplas, a sintaxe é válida
            triple_count = len(self.graph)
            result.details['triple_count'] = triple_count
            
            if triple_count == 0:
                result.add_warning("O grafo está vazio (0 triplas)")
            else:
                result.details['message'] = f"Sintaxe válida: {triple_count} triplas carregadas"
        
        except Exception as e:
            result.add_error(f"Erro ao validar sintaxe: {str(e)}")
        
        return result
    
    def validate_classes(self, expected_classes: List[str]) -> ValidationResult:
        """
        Valida a presença de classes esperadas no schema.
        
        Args:
            expected_classes: Lista de nomes de classes esperadas (sem prefixo)
        
        Returns:
            ValidationResult indicando quais classes foram encontradas
        """
        result = ValidationResult(is_valid=True)
        found_classes = []
        missing_classes = []
        
        for class_name in expected_classes:
            class_uri = self.rec[class_name]
            
            # Verifica se a classe está definida como owl:Class
            if (class_uri, RDF.type, OWL.Class) in self.graph:
                found_classes.append(class_name)
            else:
                missing_classes.append(class_name)
                result.add_error(f"Classe esperada não encontrada: {class_name}")
        
        result.details['found_classes'] = found_classes
        result.details['missing_classes'] = missing_classes
        result.details['total_expected'] = len(expected_classes)
        result.details['total_found'] = len(found_classes)
        
        return result
    
    def validate_properties(self) -> ValidationResult:
        """
        Valida propriedades de objeto e suas restrições (domain/range).
        
        Returns:
            ValidationResult com informações sobre propriedades encontradas
        """
        result = ValidationResult(is_valid=True)
        
        # Busca todas as propriedades de objeto
        object_properties = []
        for s, p, o in self.graph.triples((None, RDF.type, OWL.ObjectProperty)):
            prop_name = str(s).split('#')[-1] if '#' in str(s) else str(s)
            
            # Verifica domain e range
            domain = None
            range_val = None
            
            for _, _, d in self.graph.triples((s, RDFS.domain, None)):
                domain = str(d).split('#')[-1] if '#' in str(d) else str(d)
            
            for _, _, r in self.graph.triples((s, RDFS.range, None)):
                range_val = str(r).split('#')[-1] if '#' in str(r) else str(r)
            
            object_properties.append({
                'name': prop_name,
                'domain': domain,
                'range': range_val
            })
            
            # Aviso se domain ou range não estão definidos
            if not domain:
                result.add_warning(f"Propriedade '{prop_name}' sem domain definido")
            if not range_val:
                result.add_warning(f"Propriedade '{prop_name}' sem range definido")
        
        result.details['object_properties'] = object_properties
        result.details['total_properties'] = len(object_properties)
        
        if len(object_properties) == 0:
            result.add_warning("Nenhuma propriedade de objeto encontrada")
        
        return result
    
    def validate_disjointness(self) -> ValidationResult:
        """
        Valida restrições disjointWith entre classes.
        
        Returns:
            ValidationResult com informações sobre restrições de disjunção
        """
        result = ValidationResult(is_valid=True)
        disjoint_pairs = []
        
        # Busca todas as restrições disjointWith
        for s, p, o in self.graph.triples((None, OWL.disjointWith, None)):
            class1 = str(s).split('#')[-1] if '#' in str(s) else str(s)
            class2 = str(o).split('#')[-1] if '#' in str(o) else str(o)
            disjoint_pairs.append((class1, class2))
        
        result.details['disjoint_pairs'] = disjoint_pairs
        result.details['total_disjoint_constraints'] = len(disjoint_pairs)
        
        if len(disjoint_pairs) == 0:
            result.add_warning("Nenhuma restrição disjointWith encontrada")
        else:
            result.details['message'] = f"Encontradas {len(disjoint_pairs)} restrições de disjunção"
        
        return result
    
    def validate_instances(self) -> ValidationResult:
        """
        Valida tipagem de instâncias na base de conhecimento.
        
        Verifica se as instâncias estão corretamente tipadas com classes da ontologia.
        
        Returns:
            ValidationResult com informações sobre instâncias
        """
        result = ValidationResult(is_valid=True)
        instances_by_class = {}
        untyped_instances = []
        
        # Busca todas as instâncias (sujeitos que não são classes ou propriedades)
        all_subjects = set(self.graph.subjects())
        
        for subject in all_subjects:
            # Ignora URIs de classes e propriedades
            if (subject, RDF.type, OWL.Class) in self.graph:
                continue
            if (subject, RDF.type, OWL.ObjectProperty) in self.graph:
                continue
            if (subject, RDF.type, RDFS.Class) in self.graph:
                continue
            
            # Busca os tipos da instância
            types = list(self.graph.objects(subject, RDF.type))
            
            if not types:
                instance_name = str(subject).split('#')[-1] if '#' in str(subject) else str(subject)
                untyped_instances.append(instance_name)
            else:
                for type_uri in types:
                    # Ignora tipos OWL/RDF/RDFS
                    if str(type_uri).startswith('http://www.w3.org/'):
                        continue
                    
                    class_name = str(type_uri).split('#')[-1] if '#' in str(type_uri) else str(type_uri)
                    
                    if class_name not in instances_by_class:
                        instances_by_class[class_name] = []
                    
                    instance_name = str(subject).split('#')[-1] if '#' in str(subject) else str(subject)
                    instances_by_class[class_name].append(instance_name)
        
        result.details['instances_by_class'] = instances_by_class
        result.details['untyped_instances'] = untyped_instances
        result.details['total_classes_with_instances'] = len(instances_by_class)
        
        total_instances = sum(len(instances) for instances in instances_by_class.values())
        result.details['total_instances'] = total_instances
        
        if untyped_instances:
            result.add_warning(f"{len(untyped_instances)} instâncias sem tipo encontradas")
        
        if total_instances == 0:
            result.add_warning("Nenhuma instância encontrada na base de conhecimento")
        
        return result
    
    def generate_report(self) -> str:
        """
        Gera relatório completo de validação da ontologia.
        
        Returns:
            String formatada com o relatório completo
        """
        output = []
        output.append("=" * 80)
        output.append("RELATÓRIO DE VALIDAÇÃO DA ONTOLOGIA")
        output.append("=" * 80)
        
        # 1. Validação de Sintaxe
        output.append("\n1. VALIDAÇÃO DE SINTAXE")
        output.append("-" * 80)
        syntax_result = self.validate_syntax()
        if syntax_result.is_valid:
            output.append(f"✓ {syntax_result.details.get('message', 'Sintaxe válida')}")
        else:
            output.append("✗ Erros de sintaxe encontrados:")
            for error in syntax_result.errors:
                output.append(f"  - {error}")
        
        # 2. Validação de Classes
        output.append("\n2. VALIDAÇÃO DE CLASSES")
        output.append("-" * 80)
        expected_classes = [
            'AgenteUrbano', 'PoderPublico', 'Comunidade', 'Mercado',
            'AcaoUrbana', 'Acao_Propositiva', 'Acao_Impeditiva',
            'InstrumentoUrbano', 'EspacoUrbano', 'DanoUrbano', 'BeneficioUrbano'
        ]
        classes_result = self.validate_classes(expected_classes)
        output.append(f"Classes encontradas: {classes_result.details['total_found']}/{classes_result.details['total_expected']}")
        
        if classes_result.details['found_classes']:
            output.append("✓ Classes presentes:")
            for cls in classes_result.details['found_classes']:
                output.append(f"  - {cls}")
        
        if classes_result.details['missing_classes']:
            output.append("✗ Classes ausentes:")
            for cls in classes_result.details['missing_classes']:
                output.append(f"  - {cls}")
        
        # 3. Validação de Propriedades
        output.append("\n3. VALIDAÇÃO DE PROPRIEDADES")
        output.append("-" * 80)
        props_result = self.validate_properties()
        output.append(f"Total de propriedades de objeto: {props_result.details['total_properties']}")
        
        if props_result.details['object_properties']:
            for prop in props_result.details['object_properties']:
                domain_str = prop['domain'] if prop['domain'] else "não definido"
                range_str = prop['range'] if prop['range'] else "não definido"
                output.append(f"  - {prop['name']}: {domain_str} → {range_str}")
        
        # 4. Validação de Disjunção
        output.append("\n4. VALIDAÇÃO DE RESTRIÇÕES DISJOINTWITH")
        output.append("-" * 80)
        disjoint_result = self.validate_disjointness()
        output.append(f"Total de restrições: {disjoint_result.details['total_disjoint_constraints']}")
        
        if disjoint_result.details['disjoint_pairs']:
            for class1, class2 in disjoint_result.details['disjoint_pairs']:
                output.append(f"  - {class1} ⊥ {class2}")
        
        # 5. Validação de Instâncias
        output.append("\n5. VALIDAÇÃO DE INSTÂNCIAS")
        output.append("-" * 80)
        instances_result = self.validate_instances()
        output.append(f"Total de instâncias: {instances_result.details['total_instances']}")
        output.append(f"Classes com instâncias: {instances_result.details['total_classes_with_instances']}")
        
        if instances_result.details['instances_by_class']:
            for class_name, instances in instances_result.details['instances_by_class'].items():
                output.append(f"  - {class_name}: {len(instances)} instância(s)")
        
        # Resumo de Avisos e Erros
        all_warnings = (syntax_result.warnings + classes_result.warnings + 
                       props_result.warnings + disjoint_result.warnings + 
                       instances_result.warnings)
        all_errors = (syntax_result.errors + classes_result.errors + 
                     props_result.errors + disjoint_result.errors + 
                     instances_result.errors)
        
        output.append("\n" + "=" * 80)
        output.append("RESUMO")
        output.append("=" * 80)
        output.append(f"Total de avisos: {len(all_warnings)}")
        output.append(f"Total de erros: {len(all_errors)}")
        
        if all_warnings:
            output.append("\n⚠️  AVISOS:")
            for warning in all_warnings:
                output.append(f"  - {warning}")
        
        if all_errors:
            output.append("\n✗ ERROS:")
            for error in all_errors:
                output.append(f"  - {error}")
        
        if not all_errors:
            output.append("\n✓ Validação concluída com sucesso!")
        else:
            output.append("\n✗ Validação concluída com erros.")
        
        output.append("=" * 80)
        
        return "\n".join(output)
