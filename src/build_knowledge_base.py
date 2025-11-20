# src/build_knowledge_base.py
"""
ORÁCULO DE BRITO - Sistema Completo de Ontologia de Conflitos Urbanos (V5 AVANÇADA)

Este sistema modela a complexidade real dos conflitos urbanos em Recife através de:
- 7 EIXOS TEMÁTICOS: Agentes, Ações, Espaços, Instrumentos, Danos, Benefícios, Normas
- AXIOMAS FORMAIS: Disjunções, propriedades simétricas/transitivas, restrições de domínio
- INFERÊNCIA OWL-RL: Raciocínio automático sobre hierarquias e relações
- CONSULTAS SPARQL: Detecção de conflitos normativos e cadeias causais

Pipeline de Execução:
1. Construção do Schema Completo (7 eixos + axiomas)
2. Instanciação de Casos Reais (PREZEIS vs Remembramento)
3. Inferência Lógica (OWL-RL Reasoner)
4. Validação e Consultas
"""
import time
import os
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
import owlrl

# --- SETUP DE CAMINHOS ROBUSTOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Namespace principal
REC = Namespace("http://recife.leg.br/ontologia-conflito#")

def build_schema():
    """
    Constrói o Schema Completo da Ontologia com 7 Eixos Temáticos.
    
    EIXO 1: AGENTES URBANOS - Modelagem da fragmentação do poder público
    EIXO 2: AÇÕES URBANAS - Dicotomia entre ações propositivas e impeditivas
    EIXO 3: ESPAÇOS DE CONFLITO - Geografia legal com sobreposições
    EIXO 4: INSTRUMENTOS - Ferramentas fiscais, financeiras e de ordenamento
    EIXO 5: CONSEQUÊNCIAS URBANAS - Danos e benefícios como resultados de ações
    EIXO 6: NORMAS E CONFLITOS - Lógica formal do conflito legal (inclui categorias normativas)
    """
    print("=" * 80)
    print("CONSTRUINDO SCHEMA COMPLETO DA ONTOLOGIA (V5 AVANÇADA)")
    print("=" * 80)
    
    g = Graph()
    g.bind("rec", REC)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    
    # =========================================================================
    # EIXO 1: AGENTES URBANOS (OS JOGADORES DO CONFLITO)
    # =========================================================================
    print("\n[EIXO 1] Definindo Agentes Urbanos...")
    
    # Classe raiz
    g.add((REC.AgenteUrbano, RDF.type, OWL.Class))
    g.add((REC.AgenteUrbano, RDFS.label, Literal("Agente Urbano")))
    
    # Comunidade
    g.add((REC.Comunidade, RDF.type, OWL.Class))
    g.add((REC.Comunidade, RDFS.subClassOf, REC.AgenteUrbano))
    g.add((REC.Comunidade, RDFS.label, Literal("Comunidade")))
    
    # Agentes de Mercado (com papéis antagônicos)
    g.add((REC.Agente_de_Mercado, RDF.type, OWL.Class))
    g.add((REC.Agente_de_Mercado, RDFS.subClassOf, REC.AgenteUrbano))
    
    g.add((REC.Investidor_Desenvolvedor, RDF.type, OWL.Class))
    g.add((REC.Investidor_Desenvolvedor, RDFS.subClassOf, REC.Agente_de_Mercado))
    g.add((REC.Investidor_Desenvolvedor, RDFS.label, Literal("Investidor Desenvolvedor (Papel Positivo)")))
    
    g.add((REC.Agente_Especulativo, RDF.type, OWL.Class))
    g.add((REC.Agente_Especulativo, RDFS.subClassOf, REC.Agente_de_Mercado))
    g.add((REC.Agente_Especulativo, RDFS.label, Literal("Agente Especulativo (Papel Negativo)")))
    
    # AXIOMA: Um agente não pode ser desenvolvedor E especulativo simultaneamente
    g.add((REC.Investidor_Desenvolvedor, OWL.disjointWith, REC.Agente_Especulativo))
    
    # Poder Público (fragmentado em múltiplas agências)
    g.add((REC.PoderPublico, RDF.type, OWL.Class))
    g.add((REC.PoderPublico, RDFS.subClassOf, REC.AgenteUrbano))
    g.add((REC.PoderPublico, RDFS.label, Literal("Poder Público")))
    
    g.add((REC.AgenteExecutivo, RDF.type, OWL.Class))
    g.add((REC.AgenteExecutivo, RDFS.subClassOf, REC.PoderPublico))
    g.add((REC.AgenteExecutivo, RDFS.label, Literal("Agente Executivo")))
    g.add((REC.AgenteExecutivo, RDFS.comment, Literal("Ramo executor (Prefeitura, SEDUL, Gabinete do Centro)")))
    
    g.add((REC.AgenteLegislativo, RDF.type, OWL.Class))
    g.add((REC.AgenteLegislativo, RDFS.subClassOf, REC.PoderPublico))
    g.add((REC.AgenteLegislativo, RDFS.label, Literal("Agente Legislativo")))
    g.add((REC.AgenteLegislativo, RDFS.comment, Literal("Ramo legislador (Câmara Municipal)")))
    
    g.add((REC.OrgaoDePreservacao, RDF.type, OWL.Class))
    g.add((REC.OrgaoDePreservacao, RDFS.subClassOf, REC.PoderPublico))
    g.add((REC.OrgaoDePreservacao, RDFS.label, Literal("Órgão de Preservação")))
    g.add((REC.OrgaoDePreservacao, RDFS.comment, Literal("Tutela sobre patrimônio (DPPC, IPHAN)")))
    
    g.add((REC.OrgaoDeControle, RDF.type, OWL.Class))
    g.add((REC.OrgaoDeControle, RDFS.subClassOf, REC.PoderPublico))
    g.add((REC.OrgaoDeControle, RDFS.label, Literal("Órgão de Controle")))
    g.add((REC.OrgaoDeControle, RDFS.comment, Literal("Auditor que fiscaliza (Ministério Público)")))
    
    g.add((REC.OrgaoParticipativo, RDF.type, OWL.Class))
    g.add((REC.OrgaoParticipativo, RDFS.subClassOf, REC.PoderPublico))
    g.add((REC.OrgaoParticipativo, RDFS.label, Literal("Órgão Participativo")))
    g.add((REC.OrgaoParticipativo, RDFS.comment, Literal("Participação social (Conselho da Cidade)")))
    
    # =========================================================================
    # EIXO 2: AÇÕES URBANAS (OS MOVIMENTOS)
    # =========================================================================
    print("[EIXO 2] Definindo Ações Urbanas...")
    
    g.add((REC.AcaoUrbana, RDF.type, OWL.Class))
    g.add((REC.AcaoUrbana, RDFS.label, Literal("Ação Urbana")))
    
    g.add((REC.Acao_Propositiva, RDF.type, OWL.Class))
    g.add((REC.Acao_Propositiva, RDFS.subClassOf, REC.AcaoUrbana))
    g.add((REC.Acao_Propositiva, RDFS.label, Literal("Ação Propositiva")))
    
    g.add((REC.Acao_Impeditiva, RDF.type, OWL.Class))
    g.add((REC.Acao_Impeditiva, RDFS.subClassOf, REC.AcaoUrbana))
    g.add((REC.Acao_Impeditiva, RDFS.label, Literal("Ação Impeditiva (Veto/Inação)")))
    
    # AXIOMA: Ações propositivas e impeditivas são mutuamente exclusivas
    g.add((REC.Acao_Propositiva, OWL.disjointWith, REC.Acao_Impeditiva))
    
    # =========================================================================
    # EIXO 3: ESPAÇOS DE CONFLITO (O TABULEIRO)
    # =========================================================================
    print("[EIXO 3] Definindo Espaços de Conflito...")
    
    g.add((REC.EspacoDeConflito, RDF.type, OWL.Class))
    g.add((REC.EspacoDeConflito, RDFS.label, Literal("Espaço de Conflito")))
    
    # Zonas de Interesse Social
    g.add((REC.ZEIS, RDF.type, OWL.Class))
    g.add((REC.ZEIS, RDFS.subClassOf, REC.EspacoDeConflito))
    g.add((REC.ZEIS, RDFS.label, Literal("ZEIS - Zona Especial de Interesse Social")))
    
    g.add((REC.Centro_Ocioso, RDF.type, OWL.Class))
    g.add((REC.Centro_Ocioso, RDFS.subClassOf, REC.EspacoDeConflito))
    g.add((REC.Centro_Ocioso, RDFS.label, Literal("Centro Ocioso")))
    
    # Geografia Legal (Sobreposição de Camadas)
    g.add((REC.ZonaDePreservacao, RDF.type, OWL.Class))
    g.add((REC.ZonaDePreservacao, RDFS.subClassOf, REC.EspacoDeConflito))
    g.add((REC.ZonaDePreservacao, RDFS.label, Literal("Zona de Preservação (Patrimônio)")))
    
    g.add((REC.ZEPH, RDF.type, OWL.Class))
    g.add((REC.ZEPH, RDFS.subClassOf, REC.ZonaDePreservacao))
    g.add((REC.ZEPH, RDFS.label, Literal("ZEPH - Zona Especial de Preservação do Patrimônio")))
    
    g.add((REC.IEP, RDF.type, OWL.Class))
    g.add((REC.IEP, RDFS.subClassOf, REC.ZonaDePreservacao))
    g.add((REC.IEP, RDFS.label, Literal("IEP - Imóvel Especial de Preservação")))
    
    g.add((REC.SPR, RDF.type, OWL.Class))
    g.add((REC.SPR, RDFS.subClassOf, REC.ZEPH))
    g.add((REC.SPR, RDFS.label, Literal("SPR - Setor de Preservação Rigorosa")))
    
    # Zonas de Aplicação de Instrumentos
    g.add((REC.ZonaDeAplicacaoDeInstrumento, RDF.type, OWL.Class))
    g.add((REC.ZonaDeAplicacaoDeInstrumento, RDFS.subClassOf, REC.EspacoDeConflito))
    
    g.add((REC.AreaRecentro, RDF.type, OWL.Class))
    g.add((REC.AreaRecentro, RDFS.subClassOf, REC.ZonaDeAplicacaoDeInstrumento))
    g.add((REC.AreaRecentro, RDFS.label, Literal("Área de Aplicação do Recentro")))
    
    g.add((REC.AreaCedenteTDC, RDF.type, OWL.Class))
    g.add((REC.AreaCedenteTDC, RDFS.subClassOf, REC.ZonaDeAplicacaoDeInstrumento))
    g.add((REC.AreaCedenteTDC, RDFS.label, Literal("Área Cedente de TDC")))
    
    g.add((REC.AreaReceptoraTDC, RDF.type, OWL.Class))
    g.add((REC.AreaReceptoraTDC, RDFS.subClassOf, REC.ZonaDeAplicacaoDeInstrumento))
    g.add((REC.AreaReceptoraTDC, RDFS.label, Literal("Área Receptora de TDC")))
    
    g.add((REC.AreaReceptoraBonus, RDF.type, OWL.Class))
    g.add((REC.AreaReceptoraBonus, RDFS.subClassOf, REC.ZonaDeAplicacaoDeInstrumento))
    g.add((REC.AreaReceptoraBonus, RDFS.label, Literal("Área Receptora de Bônus Construtivo")))
    
    # =========================================================================
    # EIXO 4: INSTRUMENTOS (AS FERRAMENTAS)
    # =========================================================================
    print("[EIXO 4] Definindo Instrumentos Urbanísticos...")
    
    g.add((REC.InstrumentoAcao, RDF.type, OWL.Class))
    g.add((REC.InstrumentoAcao, RDFS.label, Literal("Instrumento & Ação")))
    
    g.add((REC.PEUC, RDF.type, OWL.Class))
    g.add((REC.PEUC, RDFS.subClassOf, REC.InstrumentoAcao))
    g.add((REC.PEUC, RDFS.label, Literal("PEUC - Parcelamento, Edificação ou Utilização Compulsórios")))
    
    g.add((REC.OODC, RDF.type, OWL.Class))
    g.add((REC.OODC, RDFS.subClassOf, REC.InstrumentoAcao))
    g.add((REC.OODC, RDFS.label, Literal("OODC - Outorga Onerosa do Direito de Construir")))
    
    # Instrumentos Fiscais e Financeiros
    g.add((REC.InstrumentoFiscalEFinanceiro, RDF.type, OWL.Class))
    g.add((REC.InstrumentoFiscalEFinanceiro, RDFS.subClassOf, REC.InstrumentoAcao))
    
    g.add((REC.IncentivoFiscal, RDF.type, OWL.Class))
    g.add((REC.IncentivoFiscal, RDFS.subClassOf, REC.InstrumentoFiscalEFinanceiro))
    
    g.add((REC.IncentivoRecentro, RDF.type, OWL.Class))
    g.add((REC.IncentivoRecentro, RDFS.subClassOf, REC.IncentivoFiscal))
    g.add((REC.IncentivoRecentro, RDFS.label, Literal("Incentivo Fiscal (Recentro)")))
    
    g.add((REC.TransferenciaDireitoDeConstruir, RDF.type, OWL.Class))
    g.add((REC.TransferenciaDireitoDeConstruir, RDFS.subClassOf, REC.InstrumentoFiscalEFinanceiro))
    g.add((REC.TransferenciaDireitoDeConstruir, RDFS.label, Literal("TDC - Transferência do Direito de Construir")))
    
    g.add((REC.BonusConstrutivo, RDF.type, OWL.Class))
    g.add((REC.BonusConstrutivo, RDFS.subClassOf, REC.InstrumentoFiscalEFinanceiro))
    g.add((REC.BonusConstrutivo, RDFS.label, Literal("Bônus Construtivo")))
    
    # Instrumentos de Ordenamento Físico
    g.add((REC.InstrumentoDeOrdenamentoFisico, RDF.type, OWL.Class))
    g.add((REC.InstrumentoDeOrdenamentoFisico, RDFS.subClassOf, REC.InstrumentoAcao))
    
    g.add((REC.RemembramentoDeLotes, RDF.type, OWL.Class))
    g.add((REC.RemembramentoDeLotes, RDFS.subClassOf, REC.InstrumentoDeOrdenamentoFisico))
    g.add((REC.RemembramentoDeLotes, RDFS.label, Literal("Remembramento de Lotes")))
    
    # =========================================================================
    # EIXO 5: CONSEQUÊNCIAS URBANAS (RESULTADOS DE AÇÕES)
    # =========================================================================
    print("[EIXO 5] Definindo Consequências Urbanas...")
    
    # Superclasse: ConsequenciaUrbana
    g.add((REC.ConsequenciaUrbana, RDF.type, OWL.Class))
    g.add((REC.ConsequenciaUrbana, RDFS.label, Literal("Consequência Urbana")))
    g.add((REC.ConsequenciaUrbana, RDFS.comment, Literal("Superclasse para resultados de ações urbanas (positivos ou negativos)")))
    
    # Subclasse: Danos Urbanos
    g.add((REC.DanoUrbano, RDF.type, OWL.Class))
    g.add((REC.DanoUrbano, RDFS.subClassOf, REC.ConsequenciaUrbana))
    g.add((REC.DanoUrbano, RDFS.label, Literal("Dano Urbano")))
    
    g.add((REC.Caos_Funcional, RDF.type, OWL.Class))
    g.add((REC.Caos_Funcional, RDFS.subClassOf, REC.DanoUrbano))
    g.add((REC.Caos_Funcional, RDFS.label, Literal("Caos Funcional")))
    
    g.add((REC.Arrecadacao_Perdida, RDF.type, OWL.Class))
    g.add((REC.Arrecadacao_Perdida, RDFS.subClassOf, REC.DanoUrbano))
    g.add((REC.Arrecadacao_Perdida, RDFS.label, Literal("Arrecadação Perdida")))
    
    g.add((REC.Doenca_e_Morte, RDF.type, OWL.Class))
    g.add((REC.Doenca_e_Morte, RDFS.subClassOf, REC.DanoUrbano))
    g.add((REC.Doenca_e_Morte, RDFS.label, Literal("Doença e Morte")))
    
    # Subclasse: Benefícios Urbanos
    g.add((REC.BeneficioUrbano, RDF.type, OWL.Class))
    g.add((REC.BeneficioUrbano, RDFS.subClassOf, REC.ConsequenciaUrbana))
    g.add((REC.BeneficioUrbano, RDFS.label, Literal("Benefício Urbano")))
    
    g.add((REC.Ordem_Funcional, RDF.type, OWL.Class))
    g.add((REC.Ordem_Funcional, RDFS.subClassOf, REC.BeneficioUrbano))
    g.add((REC.Ordem_Funcional, RDFS.label, Literal("Ordem Funcional")))
    
    g.add((REC.Arrecadacao_Aumentada, RDF.type, OWL.Class))
    g.add((REC.Arrecadacao_Aumentada, RDFS.subClassOf, REC.BeneficioUrbano))
    g.add((REC.Arrecadacao_Aumentada, RDFS.label, Literal("Arrecadação Aumentada")))
    
    g.add((REC.Dignidade_Social, RDF.type, OWL.Class))
    g.add((REC.Dignidade_Social, RDFS.subClassOf, REC.BeneficioUrbano))
    g.add((REC.Dignidade_Social, RDFS.label, Literal("Dignidade Social")))
    
    # AXIOMA CRÍTICO: Benefícios e Danos são mutuamente exclusivos
    g.add((REC.BeneficioUrbano, OWL.disjointWith, REC.DanoUrbano))
    g.add((REC.BeneficioUrbano, RDFS.comment, Literal("Disjunto de DanoUrbano - uma consequência não pode ser benefício E dano")))
    g.add((REC.DanoUrbano, RDFS.comment, Literal("Disjunto de BeneficioUrbano - uma consequência não pode ser dano E benefício")))
    
    # =========================================================================
    # EIXO 7: NORMAS E CONFLITOS (A LÓGICA DO JOGO)
    # =========================================================================
    print("[EIXO 7] Definindo Normas e Conflitos Legais...")
    
    g.add((REC.Norma, RDF.type, OWL.Class))
    g.add((REC.Norma, RDFS.label, Literal("Norma Jurídica")))
    g.add((REC.Norma, RDFS.comment, Literal("Classe pai para todas as regras, leis e processos")))
    
    g.add((REC.LegislacaoUrbana, RDF.type, OWL.Class))
    g.add((REC.LegislacaoUrbana, RDFS.subClassOf, REC.Norma))
    g.add((REC.LegislacaoUrbana, RDFS.label, Literal("Legislação Urbana (Lei)")))
    
    g.add((REC.ProjetoDeLei, RDF.type, OWL.Class))
    g.add((REC.ProjetoDeLei, RDFS.subClassOf, REC.Norma))
    g.add((REC.ProjetoDeLei, RDFS.label, Literal("Projeto de Lei (PL)")))
    
    g.add((REC.ArtigoDeLei, RDF.type, OWL.Class))
    g.add((REC.ArtigoDeLei, RDFS.subClassOf, REC.Norma))
    g.add((REC.ArtigoDeLei, RDFS.label, Literal("Artigo de Lei")))
    
    g.add((REC.ProcessoLegislativo, RDF.type, OWL.Class))
    g.add((REC.ProcessoLegislativo, RDFS.subClassOf, REC.Norma))
    g.add((REC.ProcessoLegislativo, RDFS.label, Literal("Processo Legislativo")))
    
    # Categorias Normativas (conceitos legais abstratos)
    g.add((REC.CategoriaNormativa, RDF.type, OWL.Class))
    g.add((REC.CategoriaNormativa, RDFS.subClassOf, REC.Norma))
    g.add((REC.CategoriaNormativa, RDFS.label, Literal("Categoria Normativa")))
    g.add((REC.CategoriaNormativa, RDFS.comment, Literal("Conceito legal abstrato que classifica espaços (ex: ZEIS, ZEPH)")))
    
    g.add((REC.Categoria_ZEIS, RDF.type, OWL.Class))
    g.add((REC.Categoria_ZEIS, RDFS.subClassOf, REC.CategoriaNormativa))
    g.add((REC.Categoria_ZEIS, RDFS.label, Literal("Categoria ZEIS (Norma)")))
    g.add((REC.Categoria_ZEIS, RDFS.comment, Literal("Conceito legal de ZEIS como categoria normativa")))
    
    print("\n" + "=" * 80)
    print("DEFININDO PROPRIEDADES E AXIOMAS")
    print("=" * 80)
    
    # =========================================================================
    # PROPRIEDADES BÁSICAS (V4 Revisadas)
    # =========================================================================
    print("\n[PROPRIEDADES] Definindo relações básicas...")
    
    # executaAcao: Agente → Ação
    g.add((REC.executaAcao, RDF.type, OWL.ObjectProperty))
    g.add((REC.executaAcao, RDFS.domain, REC.AgenteUrbano))
    g.add((REC.executaAcao, RDFS.range, REC.AcaoUrbana))
    g.add((REC.executaAcao, RDFS.comment, Literal("Conecta um agente à ação que ele executa")))
    
    # utilizaInstrumento: Ação → Instrumento (CORREÇÃO V5: permite ações impeditivas)
    g.add((REC.utilizaInstrumento, RDF.type, OWL.ObjectProperty))
    g.add((REC.utilizaInstrumento, RDFS.domain, REC.AcaoUrbana))
    g.add((REC.utilizaInstrumento, RDFS.range, REC.InstrumentoAcao))
    g.add((REC.utilizaInstrumento, RDFS.comment, Literal("Ação utiliza um instrumento (pode ser positivo ou negativo)")))
    
    # causa_direta: Ação Impeditiva → Dano (especialização)
    g.add((REC.causa_direta, RDF.type, OWL.ObjectProperty))
    g.add((REC.causa_direta, RDFS.subPropertyOf, REC.gera_consequencia))
    g.add((REC.causa_direta, RDFS.domain, REC.Acao_Impeditiva))
    g.add((REC.causa_direta, RDFS.range, REC.DanoUrbano))
    g.add((REC.causa_direta, RDFS.comment, Literal("Relação causal: ação impeditiva causa dano urbano")))
    
    # gera_consequencia: Ação → Consequência (propriedade genérica)
    g.add((REC.gera_consequencia, RDF.type, OWL.ObjectProperty))
    g.add((REC.gera_consequencia, RDFS.domain, REC.AcaoUrbana))
    g.add((REC.gera_consequencia, RDFS.range, REC.ConsequenciaUrbana))
    g.add((REC.gera_consequencia, RDFS.comment, Literal("Propriedade genérica: ação gera consequência (positiva ou negativa)")))
    
    # gera_beneficio: Ação Propositiva → Benefício (especialização)
    g.add((REC.gera_beneficio, RDF.type, OWL.ObjectProperty))
    g.add((REC.gera_beneficio, RDFS.subPropertyOf, REC.gera_consequencia))
    g.add((REC.gera_beneficio, RDFS.domain, REC.Acao_Propositiva))
    g.add((REC.gera_beneficio, RDFS.range, REC.BeneficioUrbano))
    g.add((REC.gera_beneficio, RDFS.comment, Literal("Relação positiva: ação propositiva gera benefício")))
    
    # e_reversao_de: Benefício → Dano
    g.add((REC.e_reversao_de, RDF.type, OWL.ObjectProperty))
    g.add((REC.e_reversao_de, RDFS.domain, REC.BeneficioUrbano))
    g.add((REC.e_reversao_de, RDFS.range, REC.DanoUrbano))
    g.add((REC.e_reversao_de, RDFS.comment, Literal("Benefício reverte um dano específico")))
    
    # em_antagonismo_com: Agente ↔ Agente (SIMÉTRICA)
    g.add((REC.em_antagonismo_com, RDF.type, OWL.SymmetricProperty))
    g.add((REC.em_antagonismo_com, RDF.type, OWL.ObjectProperty))
    g.add((REC.em_antagonismo_com, RDFS.domain, REC.AgenteUrbano))
    g.add((REC.em_antagonismo_com, RDFS.range, REC.AgenteUrbano))
    g.add((REC.em_antagonismo_com, RDFS.comment, Literal("Relação simétrica de disputa entre agentes")))
    
    # =========================================================================
    # PROPRIEDADES AVANÇADAS (V5 - AGÊNCIA E AUDITORIA)
    # =========================================================================
    print("[PROPRIEDADES] Definindo relações avançadas de agência...")
    
    # temAtribuicaoLegal: Poder Público → String
    g.add((REC.temAtribuicaoLegal, RDF.type, OWL.DatatypeProperty))
    g.add((REC.temAtribuicaoLegal, RDFS.domain, REC.PoderPublico))
    g.add((REC.temAtribuicaoLegal, RDFS.range, XSD.string))
    g.add((REC.temAtribuicaoLegal, RDFS.comment, Literal("Codifica o poder legal de um agente")))
    
    # exerceTutelaSobre: Órgão de Preservação → Espaço
    g.add((REC.exerceTutelaSobre, RDF.type, OWL.ObjectProperty))
    g.add((REC.exerceTutelaSobre, RDFS.domain, REC.OrgaoDePreservacao))
    g.add((REC.exerceTutelaSobre, RDFS.range, REC.EspacoDeConflito))
    g.add((REC.exerceTutelaSobre, RDFS.comment, Literal("Mapeia jurisdição de órgão sobre espaço")))
    
    # recomendaAcao: Órgão de Controle → Ação
    g.add((REC.recomendaAcao, RDF.type, OWL.ObjectProperty))
    g.add((REC.recomendaAcao, RDFS.domain, REC.OrgaoDeControle))
    g.add((REC.recomendaAcao, RDFS.range, REC.AcaoUrbana))
    g.add((REC.recomendaAcao, RDFS.comment, Literal("Ação corretiva emitida por auditor")))
    
    # interageCom: Agente Executivo → Órgão de Preservação
    g.add((REC.interageCom, RDF.type, OWL.ObjectProperty))
    g.add((REC.interageCom, RDFS.domain, REC.AgenteExecutivo))
    g.add((REC.interageCom, RDFS.range, REC.OrgaoDePreservacao))
    g.add((REC.interageCom, RDFS.comment, Literal("Processo de aprovação entre agências")))
    
    # =========================================================================
    # PROPRIEDADES DE ESPAÇO (SOBREPOSIÇÃO LEGAL)
    # =========================================================================
    print("[PROPRIEDADES] Definindo relações espaciais...")
    
    # coincideCom: Espaço ↔ Espaço (SIMÉTRICA E TRANSITIVA)
    g.add((REC.coincideCom, RDF.type, OWL.SymmetricProperty))
    g.add((REC.coincideCom, RDF.type, OWL.TransitiveProperty))
    g.add((REC.coincideCom, RDF.type, OWL.ObjectProperty))
    g.add((REC.coincideCom, RDFS.domain, REC.EspacoDeConflito))
    g.add((REC.coincideCom, RDFS.range, REC.EspacoDeConflito))
    g.add((REC.coincideCom, RDFS.comment, Literal("Sobreposição legal de zonas (simétrica e transitiva)")))
    
    # permiteRemembramento: Espaço → Boolean
    g.add((REC.permiteRemembramento, RDF.type, OWL.DatatypeProperty))
    g.add((REC.permiteRemembramento, RDFS.domain, REC.EspacoDeConflito))
    g.add((REC.permiteRemembramento, RDFS.range, XSD.boolean))
    g.add((REC.permiteRemembramento, RDFS.comment, Literal("Interruptor lógico do conflito do PL 12/2024")))
    
    # estaSobPressaoImobiliaria: ZEIS → Agente de Mercado
    g.add((REC.estaSobPressaoImobiliaria, RDF.type, OWL.ObjectProperty))
    g.add((REC.estaSobPressaoImobiliaria, RDFS.domain, REC.ZEIS))
    g.add((REC.estaSobPressaoImobiliaria, RDFS.range, REC.Agente_de_Mercado))
    g.add((REC.estaSobPressaoImobiliaria, RDFS.comment, Literal("Pressão de gentrificação sobre ZEIS")))
    
    # =========================================================================
    # PROPRIEDADES DE INSTRUMENTOS
    # =========================================================================
    print("[PROPRIEDADES] Definindo relações de instrumentos...")
    
    # aplicaIncentivoEm: Incentivo → Espaço
    g.add((REC.aplicaIncentivoEm, RDF.type, OWL.ObjectProperty))
    g.add((REC.aplicaIncentivoEm, RDFS.domain, REC.IncentivoFiscal))
    g.add((REC.aplicaIncentivoEm, RDFS.range, REC.EspacoDeConflito))
    
    # permiteTransferirDe: TDC → Área Cedente
    g.add((REC.permiteTransferirDe, RDF.type, OWL.ObjectProperty))
    g.add((REC.permiteTransferirDe, RDFS.domain, REC.TransferenciaDireitoDeConstruir))
    g.add((REC.permiteTransferirDe, RDFS.range, REC.AreaCedenteTDC))
    
    # permiteTransferirPara: TDC → Área Receptora
    g.add((REC.permiteTransferirPara, RDF.type, OWL.ObjectProperty))
    g.add((REC.permiteTransferirPara, RDFS.domain, REC.TransferenciaDireitoDeConstruir))
    g.add((REC.permiteTransferirPara, RDFS.range, REC.AreaReceptoraTDC))
    
    # geraBonusPara: Bônus → Área Receptora
    g.add((REC.geraBonusPara, RDF.type, OWL.ObjectProperty))
    g.add((REC.geraBonusPara, RDFS.domain, REC.BonusConstrutivo))
    g.add((REC.geraBonusPara, RDFS.range, REC.AreaReceptoraBonus))
    
    # multiplicadorBonus: Bônus → Decimal
    g.add((REC.multiplicadorBonus, RDF.type, OWL.DatatypeProperty))
    g.add((REC.multiplicadorBonus, RDFS.domain, REC.BonusConstrutivo))
    g.add((REC.multiplicadorBonus, RDFS.range, XSD.decimal))
    g.add((REC.multiplicadorBonus, RDFS.comment, Literal("Multiplicador do bônus (1.0 geral, 2.0 HIS)")))
    
    # =========================================================================
    # PROPRIEDADES DE NORMAS E CONFLITOS (O NÚCLEO LÓGICO)
    # =========================================================================
    print("[PROPRIEDADES] Definindo relações de conflito normativo...")
    
    # institui: Lei → Instrumento/Órgão
    g.add((REC.institui, RDF.type, OWL.ObjectProperty))
    g.add((REC.institui, RDFS.domain, REC.LegislacaoUrbana))
    g.add((REC.institui, RDFS.range, OWL.Thing))
    g.add((REC.institui, RDFS.comment, Literal("Lei institui instrumento ou órgão")))
    
    # conflitaCom: Norma ↔ Norma (SIMÉTRICA - AXIOMA CRÍTICO)
    g.add((REC.conflitaCom, RDF.type, OWL.SymmetricProperty))
    g.add((REC.conflitaCom, RDF.type, OWL.ObjectProperty))
    g.add((REC.conflitaCom, RDFS.domain, REC.Norma))
    g.add((REC.conflitaCom, RDFS.range, REC.Norma))
    g.add((REC.conflitaCom, RDFS.comment, Literal("Declaração de inconsistência legal (simétrica)")))
    
    # permiteExcecao: Norma → Ação Impeditiva
    g.add((REC.permiteExcecao, RDF.type, OWL.ObjectProperty))
    g.add((REC.permiteExcecao, RDFS.domain, REC.Norma))
    g.add((REC.permiteExcecao, RDFS.range, REC.Acao_Impeditiva))
    g.add((REC.permiteExcecao, RDFS.comment, Literal("BRECHA LEGAL: norma permite ação que causa dano")))
    
    # violaProcessoDe: Processo → Órgão Participativo
    g.add((REC.violaProcessoDe, RDF.type, OWL.ObjectProperty))
    g.add((REC.violaProcessoDe, RDFS.domain, REC.ProcessoLegislativo))
    g.add((REC.violaProcessoDe, RDFS.range, REC.OrgaoParticipativo))
    g.add((REC.violaProcessoDe, RDFS.comment, Literal("Conflito processual")))
    
    # eImpugnadoPor: Norma → Órgão de Controle
    g.add((REC.eImpugnadoPor, RDF.type, OWL.ObjectProperty))
    g.add((REC.eImpugnadoPor, RDFS.domain, REC.Norma))
    g.add((REC.eImpugnadoPor, RDFS.range, REC.OrgaoDeControle))
    g.add((REC.eImpugnadoPor, RDFS.comment, Literal("Resposta ao conflito: impugnação")))
    
    # classifica: Categoria Normativa → Espaço
    g.add((REC.classifica, RDF.type, OWL.ObjectProperty))
    g.add((REC.classifica, RDFS.domain, REC.CategoriaNormativa))
    g.add((REC.classifica, RDFS.range, REC.EspacoDeConflito))
    g.add((REC.classifica, RDFS.comment, Literal("Categoria normativa classifica um espaço físico (ex: Categoria_ZEIS classifica ZEIS_Coque)")))
    
    # =========================================================================
    # SALVAR SCHEMA
    # =========================================================================
    output_path = os.path.join(DATA_DIR, "ontologia_conflito_urbano_schema_v5.ttl")
    g.serialize(destination=output_path, format="turtle")
    
    print("\n" + "=" * 80)
    print(f"✓ SCHEMA V5 COMPLETO SALVO EM: {output_path}")
    print(f"✓ Total de triplas (axiomas + definições): {len(g)}")
    print("=" * 80)
    
    return output_path

def populate_instances(schema_path):
    """
    Instancia o Conflito Urbano Real: PREZEIS vs Remembramento.
    
    CASO DE ESTUDO:
    - Lei do PREZEIS (1995): Protege comunidades de baixa renda
    - Lei do Remembramento (2020): Permite fusão de lotes em ZEIS
    - CONFLITO: Remembramento pode facilitar gentrificação
    """
    print("\n" + "=" * 80)
    print("INSTANCIANDO CONFLITO URBANO: PREZEIS vs REMEMBRAMENTO")
    print("=" * 80)
    
    g = Graph()
    g.parse(schema_path, format="turtle")
    
    # =========================================================================
    # AGENTES DO CONFLITO
    # =========================================================================
    print("\n[INSTÂNCIAS] Criando agentes...")
    
    agents = {
        "Prefeitura_do_Recife": (REC.AgenteExecutivo, "Prefeitura do Recife"),
        "Camara_Municipal_do_Recife": (REC.AgenteLegislativo, "Câmara Municipal do Recife"),
        "Comunidade_do_Coque": (REC.Comunidade, "Comunidade do Coque"),
        "Mercado_Imobiliario_Especulativo": (REC.Agente_Especulativo, "Mercado Imobiliário Especulativo"),
        "DPPC_Recife": (REC.OrgaoDePreservacao, "DPPC - Diretoria de Preservação do Patrimônio Cultural"),
        "Ministerio_Publico_PE": (REC.OrgaoDeControle, "Ministério Público de Pernambuco"),
        "Conselho_da_Cidade": (REC.OrgaoParticipativo, "Conselho da Cidade do Recife")
    }
    
    for name, (cls, label) in agents.items():
        g.add((REC[name], RDF.type, cls))
        g.add((REC[name], RDFS.label, Literal(label)))
    
    # =========================================================================
    # NORMAS E LEIS
    # =========================================================================
    print("[INSTÂNCIAS] Criando normas e leis...")
    
    laws = {
        "Lei_do_PREZEIS_1995": (REC.LegislacaoUrbana, "Lei do PREZEIS (1995)"),
        "Lei_do_Remembramento_2020": (REC.LegislacaoUrbana, "Lei do Remembramento (2020)"),
        "Lei_do_Recentro_2020": (REC.LegislacaoUrbana, "Lei do Recentro (2020)"),
        "PL_12_2024": (REC.ProjetoDeLei, "Projeto de Lei 12/2024 (Remembramento em ZEIS)")
    }
    
    for name, (cls, label) in laws.items():
        g.add((REC[name], RDF.type, cls))
        g.add((REC[name], RDFS.label, Literal(label)))
    
    # Categoria Normativa ZEIS
    g.add((REC.Categoria_ZEIS_Instancia, RDF.type, REC.Categoria_ZEIS))
    g.add((REC.Categoria_ZEIS_Instancia, RDFS.label, Literal("Categoria ZEIS (Conceito Legal)")))
    
    # =========================================================================
    # ESPAÇOS DE CONFLITO
    # =========================================================================
    print("[INSTÂNCIAS] Criando espaços...")
    
    spaces = {
        "ZEIS_Coque": (REC.ZEIS, "ZEIS do Coque"),
        "Centro_Historico_Recife": (REC.Centro_Ocioso, "Centro Histórico do Recife"),
        "ZEPH_Bairro_do_Recife": (REC.ZEPH, "ZEPH do Bairro do Recife"),
        "IEP_Edificio_Caixa_Dagua": (REC.IEP, "IEP - Edifício Caixa d'Água"),
        "Area_Recentro_Centro": (REC.AreaRecentro, "Área de Aplicação do Recentro no Centro")
    }
    
    for name, (cls, label) in spaces.items():
        g.add((REC[name], RDF.type, cls))
        g.add((REC[name], RDFS.label, Literal(label)))
    
    # Sobreposição espacial (AXIOMA TRANSITIVO)
    g.add((REC.IEP_Edificio_Caixa_Dagua, REC.coincideCom, REC.ZEPH_Bairro_do_Recife))
    g.add((REC.ZEPH_Bairro_do_Recife, REC.coincideCom, REC.Area_Recentro_Centro))
    # Por transitividade, o reasoner inferirá: IEP coincideCom Area_Recentro
    
    # Propriedade booleana crítica
    g.add((REC.ZEIS_Coque, REC.permiteRemembramento, Literal(False, datatype=XSD.boolean)))
    
    # =========================================================================
    # INSTRUMENTOS
    # =========================================================================
    print("[INSTÂNCIAS] Criando instrumentos...")
    
    instruments = {
        "Instrumento_PEUC": (REC.PEUC, "PEUC Aplicado no Centro"),
        "Instrumento_TDC": (REC.TransferenciaDireitoDeConstruir, "TDC do Centro Histórico"),
        "Instrumento_Remembramento": (REC.RemembramentoDeLotes, "Remembramento de Lotes"),
        "Incentivo_Recentro_Fiscal": (REC.IncentivoRecentro, "Incentivo Fiscal do Recentro")
    }
    
    for name, (cls, label) in instruments.items():
        g.add((REC[name], RDF.type, cls))
        g.add((REC[name], RDFS.label, Literal(label)))
    
    # Relações de instrumentos
    g.add((REC.Incentivo_Recentro_Fiscal, REC.aplicaIncentivoEm, REC.Area_Recentro_Centro))
    g.add((REC.Instrumento_TDC, REC.permiteTransferirDe, REC.Area_Recentro_Centro))
    
    # =========================================================================
    # AÇÕES (O CONFLITO EM MOVIMENTO)
    # =========================================================================
    print("[INSTÂNCIAS] Criando ações...")
    
    actions = {
        "Acao_Criar_Lei_PREZEIS": (REC.Acao_Propositiva, "Criar Lei do PREZEIS"),
        "Acao_Sancionar_Lei_Remembramento": (REC.Acao_Impeditiva, "Sancionar Lei do Remembramento"),
        "Acao_Omitir_Fiscalizacao_PREZEIS": (REC.Acao_Impeditiva, "Omitir Fiscalização do PREZEIS"),
        "Acao_Aplicar_PEUC": (REC.Acao_Propositiva, "Aplicar PEUC no Centro"),
        "Acao_Impugnar_PL12": (REC.Acao_Propositiva, "Impugnar PL 12/2024")
    }
    
    for name, (cls, label) in actions.items():
        g.add((REC[name], RDF.type, cls))
        g.add((REC[name], RDFS.label, Literal(label)))
    
    # =========================================================================
    # DANOS E BENEFÍCIOS
    # =========================================================================
    print("[INSTÂNCIAS] Criando danos e benefícios...")
    
    damages = {
        "Risco_de_Gentrificacao": (REC.DanoUrbano, "Risco de Gentrificação"),
        "Caos_Funcional_Centro": (REC.Caos_Funcional, "Caos Funcional no Centro"),
        "Arrecadacao_Perdida_Centro": (REC.Arrecadacao_Perdida, "Arrecadação Perdida no Centro")
    }
    
    benefits = {
        "Direito_a_Moradia": (REC.BeneficioUrbano, "Direito à Moradia"),
        "Ordem_Funcional_Centro": (REC.Ordem_Funcional, "Ordem Funcional no Centro"),
        "Arrecadacao_Aumentada_Centro": (REC.Arrecadacao_Aumentada, "Arrecadação Aumentada no Centro"),
        "Dignidade_Social_Coque": (REC.Dignidade_Social, "Dignidade Social no Coque")
    }
    
    for name, (cls, label) in damages.items():
        g.add((REC[name], RDF.type, cls))
        g.add((REC[name], RDFS.label, Literal(label)))
    
    for name, (cls, label) in benefits.items():
        g.add((REC[name], RDF.type, cls))
        g.add((REC[name], RDFS.label, Literal(label)))
    
    # =========================================================================
    # CONECTANDO A NARRATIVA (A LÓGICA DO CONFLITO)
    # =========================================================================
    print("\n[NARRATIVA] Conectando relações causais...")
    
    # Agentes executam ações
    g.add((REC.Camara_Municipal_do_Recife, REC.executaAcao, REC.Acao_Criar_Lei_PREZEIS))
    g.add((REC.Prefeitura_do_Recife, REC.executaAcao, REC.Acao_Sancionar_Lei_Remembramento))
    g.add((REC.Prefeitura_do_Recife, REC.executaAcao, REC.Acao_Omitir_Fiscalizacao_PREZEIS))
    g.add((REC.Prefeitura_do_Recife, REC.executaAcao, REC.Acao_Aplicar_PEUC))
    g.add((REC.Ministerio_Publico_PE, REC.recomendaAcao, REC.Acao_Impugnar_PL12))
    
    # Ações utilizam instrumentos
    g.add((REC.Acao_Sancionar_Lei_Remembramento, REC.utilizaInstrumento, REC.Instrumento_Remembramento))
    g.add((REC.Acao_Aplicar_PEUC, REC.utilizaInstrumento, REC.Instrumento_PEUC))
    
    # Cadeias causais (DANOS)
    g.add((REC.Acao_Sancionar_Lei_Remembramento, REC.causa_direta, REC.Risco_de_Gentrificacao))
    g.add((REC.Acao_Omitir_Fiscalizacao_PREZEIS, REC.causa_direta, REC.Risco_de_Gentrificacao))
    
    # Cadeias causais (BENEFÍCIOS)
    g.add((REC.Acao_Criar_Lei_PREZEIS, REC.gera_beneficio, REC.Direito_a_Moradia))
    g.add((REC.Acao_Criar_Lei_PREZEIS, REC.gera_beneficio, REC.Dignidade_Social_Coque))
    g.add((REC.Acao_Aplicar_PEUC, REC.gera_beneficio, REC.Ordem_Funcional_Centro))
    g.add((REC.Acao_Aplicar_PEUC, REC.gera_beneficio, REC.Arrecadacao_Aumentada_Centro))
    
    # Reversões
    g.add((REC.Ordem_Funcional_Centro, REC.e_reversao_de, REC.Caos_Funcional_Centro))
    g.add((REC.Arrecadacao_Aumentada_Centro, REC.e_reversao_de, REC.Arrecadacao_Perdida_Centro))
    
    # Antagonismos
    g.add((REC.Mercado_Imobiliario_Especulativo, REC.em_antagonismo_com, REC.Comunidade_do_Coque))
    # Por simetria, o reasoner inferirá: Comunidade em_antagonismo_com Mercado
    
    # Pressão imobiliária
    g.add((REC.ZEIS_Coque, REC.estaSobPressaoImobiliaria, REC.Mercado_Imobiliario_Especulativo))
    
    # =========================================================================
    # CONFLITO NORMATIVO (O NÚCLEO DO PROBLEMA)
    # =========================================================================
    print("[NARRATIVA] Declarando conflitos normativos...")
    
    # CONFLITO PRINCIPAL: PREZEIS vs Remembramento
    g.add((REC.Lei_do_PREZEIS_1995, REC.conflitaCom, REC.Lei_do_Remembramento_2020))
    # Por simetria, o reasoner inferirá: Remembramento conflitaCom PREZEIS
    
    # Lei institui categoria normativa e instrumentos
    g.add((REC.Lei_do_PREZEIS_1995, REC.institui, REC.Categoria_ZEIS_Instancia))
    g.add((REC.Lei_do_Remembramento_2020, REC.institui, REC.Instrumento_Remembramento))
    g.add((REC.Lei_do_Recentro_2020, REC.institui, REC.Incentivo_Recentro_Fiscal))
    
    # Categoria normativa classifica espaços físicos
    g.add((REC.Categoria_ZEIS_Instancia, REC.classifica, REC.ZEIS_Coque))
    
    # Brecha legal (permiteExcecao)
    g.add((REC.Lei_do_Remembramento_2020, REC.permiteExcecao, REC.Acao_Sancionar_Lei_Remembramento))
    
    # Impugnação
    g.add((REC.PL_12_2024, REC.eImpugnadoPor, REC.Ministerio_Publico_PE))
    
    # Tutela e interação
    g.add((REC.DPPC_Recife, REC.exerceTutelaSobre, REC.ZEPH_Bairro_do_Recife))
    g.add((REC.Prefeitura_do_Recife, REC.interageCom, REC.DPPC_Recife))
    
    # Atribuições legais
    g.add((REC.Camara_Municipal_do_Recife, REC.temAtribuicaoLegal, 
           Literal("Deliberar sobre o Plano Diretor e legislação urbanística")))
    g.add((REC.Ministerio_Publico_PE, REC.temAtribuicaoLegal, 
           Literal("Fiscalizar e impugnar atos que violem o interesse público")))
    
    # =========================================================================
    # SALVAR BASE DE CONHECIMENTO
    # =========================================================================
    output_path = os.path.join(DATA_DIR, "kb_conflito_v5_final.ttl")
    g.serialize(destination=output_path, format="turtle")
    
    print("\n" + "=" * 80)
    print(f"✓ BASE DE CONHECIMENTO INSTANCIADA SALVA EM: {output_path}")
    print(f"✓ Total de triplas (schema + instâncias): {len(g)}")
    print("=" * 80)
    
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
