"""
Visualização Gráfica da Ontologia de Conflitos Urbanos
Gera gráficos interativos e diagramas para apresentação
"""

import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Backend sem interface gráfica (para Windows)
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace, RDF, RDFS, OWL
from pyvis.network import Network
import os

REC = Namespace("http://recife.leg.br/ontologia-conflito#")

def create_class_hierarchy_graph():
    """Cria visualização da hierarquia de classes"""
    print("Gerando gráfico de hierarquia de classes...")
    
    g = Graph()
    g.parse("data/ontologia_conflito_urbano_schema_v5.ttl", format="turtle")
    
    # Criar grafo NetworkX
    G = nx.DiGraph()
    
    # Adicionar nós e arestas de subClassOf
    for s, p, o in g.triples((None, RDFS.subClassOf, None)):
        # Verificar se são URIs do namespace REC
        if str(s).startswith(str(REC)) and str(o).startswith(str(REC)):
            subclass = str(s).split('#')[-1]
            superclass = str(o).split('#')[-1]
            G.add_edge(superclass, subclass)
    
    # Configurar visualização
    plt.figure(figsize=(20, 12))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Desenhar
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=3000, font_size=10, font_weight='bold',
            arrows=True, edge_color='gray', arrowsize=20)
    
    plt.title("Hierarquia de Classes da Ontologia", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig("visualizations/class_hierarchy.png", dpi=300, bbox_inches='tight')
    print("✓ Salvo: visualizations/class_hierarchy.png")
    plt.close()

def create_interactive_graph():
    """Cria grafo interativo HTML com pyvis"""
    print("Gerando grafo interativo...")
    
    g = Graph()
    g.parse("data/kb_conflito_v5_inferido.ttl", format="turtle")
    
    net = Network(height="800px", width="100%", bgcolor="#222222", 
                  font_color="white", directed=True)
    net.barnes_hut()
    
    # Cores por tipo
    colors = {
        'Agente': '#FF6B6B',
        'Acao': '#4ECDC4',
        'Norma': '#FFE66D',
        'Espaco': '#95E1D3',
        'Instrumento': '#F38181',
        'Dano': '#AA4465',
        'Beneficio': '#6BCF7F'
    }

    
    # Adicionar nós principais
    added_nodes = set()
    for s, p, o in g.triples((None, RDF.type, None)):
        if str(s).startswith(str(REC)):
            node_id = str(s).split('#')[-1]
            if node_id not in added_nodes:
                label = str(g.value(s, RDFS.label) or node_id)
                
                # Determinar cor
                color = '#D3D3D3'
                if 'Agente' in node_id or 'Prefeitura' in node_id or 'Camara' in node_id:
                    color = colors['Agente']
                elif 'Acao' in node_id:
                    color = colors['Acao']
                elif 'Lei' in node_id or 'PL' in node_id:
                    color = colors['Norma']
                elif 'ZEIS' in node_id or 'Centro' in node_id or 'Area' in node_id:
                    color = colors['Espaco']
                elif 'Instrumento' in node_id or 'PEUC' in node_id:
                    color = colors['Instrumento']
                elif 'Risco' in node_id or 'Caos' in node_id:
                    color = colors['Dano']
                elif 'Direito' in node_id or 'Ordem' in node_id or 'Dignidade' in node_id:
                    color = colors['Beneficio']
                
                net.add_node(node_id, label=label, color=color, title=label)
                added_nodes.add(node_id)
    
    # Adicionar arestas importantes
    important_props = [REC.executaAcao, REC.conflitaCom, REC.causa_direta, 
                       REC.gera_beneficio, REC.utilizaInstrumento]
    
    for prop in important_props:
        for s, p, o in g.triples((None, prop, None)):
            if str(s).startswith(str(REC)) and str(o).startswith(str(REC)):
                source = str(s).split('#')[-1]
                target = str(o).split('#')[-1]
                edge_label = str(prop).split('#')[-1]
                
                if source in added_nodes and target in added_nodes:
                    net.add_edge(source, target, label=edge_label, title=edge_label)
    
    net.show_buttons(filter_=['physics'])
    net.save_graph("visualizations/ontology_interactive.html")
    print("✓ Salvo: visualizations/ontology_interactive.html")

def create_statistics_chart():
    """Cria gráfico de estatísticas"""
    print("Gerando gráfico de estatísticas...")
    
    # Dados
    categories = ['Schema\n(Axiomas)', 'Instâncias\n(Casos)', 'Inferido\n(Total)']
    triplas = [236, 332, 1083]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico de barras
    bars = ax1.bar(categories, triplas, color=['#4ECDC4', '#FF6B6B', '#FFE66D'])
    ax1.set_ylabel('Número de Triplas', fontsize=12, fontweight='bold')
    ax1.set_title('Evolução da Base de Conhecimento', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, value in zip(bars, triplas):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico de pizza - Composição
    labels = ['Axiomas\ne Definições', 'Instâncias\nExplícitas', 'Triplas\nInferidas']
    sizes = [236, 96, 751]
    colors_pie = ['#4ECDC4', '#FF6B6B', '#95E1D3']
    explode = (0.05, 0.05, 0.1)
    
    ax2.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax2.set_title('Composição do Grafo Inferido', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("visualizations/statistics.png", dpi=300, bbox_inches='tight')
    print("✓ Salvo: visualizations/statistics.png")
    plt.close()

def create_axioms_diagram():
    """Cria diagrama visual dos axiomas"""
    print("Gerando diagrama de axiomas...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Axiomas Formais da Ontologia', fontsize=16, fontweight='bold')
    
    # Axioma 1: Disjunção de Ações
    ax1 = axes[0, 0]
    ax1.text(0.5, 0.8, 'AXIOMA: Disjunção de Ações', ha='center', fontsize=14, fontweight='bold')
    ax1.text(0.5, 0.6, 'Acao_Propositiva ⊥ Acao_Impeditiva', ha='center', fontsize=12, 
             bbox=dict(boxstyle='round', facecolor='#FFE66D'))
    ax1.text(0.5, 0.4, '↓', ha='center', fontsize=20)
    ax1.text(0.5, 0.25, 'Uma ação NÃO PODE ser\nsimultaneamente positiva E negativa', 
             ha='center', fontsize=10)
    ax1.text(0.5, 0.05, 'Permite: Detecção de contradições', ha='center', fontsize=9, 
             style='italic', color='green')
    ax1.axis('off')
    
    # Axioma 2: Propriedade Simétrica
    ax2 = axes[0, 1]
    ax2.text(0.5, 0.8, 'AXIOMA: Propriedade Simétrica', ha='center', fontsize=14, fontweight='bold')
    ax2.text(0.5, 0.6, 'conflitaCom(A, B) → conflitaCom(B, A)', ha='center', fontsize=12,
             bbox=dict(boxstyle='round', facecolor='#FF6B6B'))
    ax2.text(0.5, 0.4, '↓', ha='center', fontsize=20)
    ax2.text(0.5, 0.25, 'Se A conflita com B\nentão B conflita com A', 
             ha='center', fontsize=10)
    ax2.text(0.5, 0.05, 'Permite: Inferência bidirecional automática', ha='center', fontsize=9,
             style='italic', color='green')
    ax2.axis('off')
    
    # Axioma 3: Propriedade Transitiva
    ax3 = axes[1, 0]
    ax3.text(0.5, 0.8, 'AXIOMA: Propriedade Transitiva', ha='center', fontsize=14, fontweight='bold')
    ax3.text(0.5, 0.6, 'coincideCom(A,B) ∧ coincideCom(B,C)\n→ coincideCom(A,C)', 
             ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='#95E1D3'))
    ax3.text(0.5, 0.4, '↓', ha='center', fontsize=20)
    ax3.text(0.5, 0.25, 'Sobreposição legal através\nde múltiplas camadas', 
             ha='center', fontsize=10)
    ax3.text(0.5, 0.05, 'Permite: Detecção de conflitos de jurisdição', ha='center', fontsize=9,
             style='italic', color='green')
    ax3.axis('off')
    
    # Axioma 4: Restrições de Domínio/Range
    ax4 = axes[1, 1]
    ax4.text(0.5, 0.8, 'AXIOMA: Restrições de Domínio', ha='center', fontsize=14, fontweight='bold')
    ax4.text(0.5, 0.6, 'causa_direta:\ndomain = Acao_Impeditiva\nrange = DanoUrbano', 
             ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='#4ECDC4'))
    ax4.text(0.5, 0.4, '↓', ha='center', fontsize=20)
    ax4.text(0.5, 0.25, 'Apenas ações impeditivas\npodem causar danos', 
             ha='center', fontsize=10)
    ax4.text(0.5, 0.05, 'Permite: Validação automática de consistência', ha='center', fontsize=9,
             style='italic', color='green')
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig("visualizations/axioms_diagram.png", dpi=300, bbox_inches='tight')
    print("✓ Salvo: visualizations/axioms_diagram.png")
    plt.close()

def create_architecture_diagram():
    """Cria diagrama de arquitetura do sistema"""
    print("Gerando diagrama de arquitetura...")
    
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Título
    ax.text(5, 9.5, 'ARQUITETURA DO SISTEMA', ha='center', fontsize=18, fontweight='bold')
    
    # Camada 1: Schema
    ax.add_patch(plt.Rectangle((0.5, 7.5), 9, 1.5, facecolor='#4ECDC4', alpha=0.7))
    ax.text(5, 8.5, 'CAMADA 1: SCHEMA (Ontologia)', ha='center', fontsize=12, fontweight='bold')
    ax.text(5, 8.1, '7 Eixos | 40+ Classes | 25+ Propriedades | 20+ Axiomas', 
            ha='center', fontsize=9)
    
    # Camada 2: Instâncias
    ax.add_patch(plt.Rectangle((0.5, 5.5), 9, 1.5, facecolor='#FF6B6B', alpha=0.7))
    ax.text(5, 6.5, 'CAMADA 2: INSTÂNCIAS (Casos Reais)', ha='center', fontsize=12, fontweight='bold')
    ax.text(5, 6.1, 'PREZEIS vs Remembramento | 30+ Indivíduos | Relações Causais', 
            ha='center', fontsize=9)
    
    # Camada 3: Reasoner
    ax.add_patch(plt.Rectangle((0.5, 3.5), 9, 1.5, facecolor='#FFE66D', alpha=0.7))
    ax.text(5, 4.5, 'CAMADA 3: REASONER OWL-RL', ha='center', fontsize=12, fontweight='bold')
    ax.text(5, 4.1, 'Inferência Automática | 332 → 1083 triplas | 0.17s', 
            ha='center', fontsize=9)
    
    # Camada 4: Consultas
    ax.add_patch(plt.Rectangle((0.5, 1.5), 9, 1.5, facecolor='#95E1D3', alpha=0.7))
    ax.text(5, 2.5, 'CAMADA 4: CONSULTAS SPARQL', ha='center', fontsize=12, fontweight='bold')
    ax.text(5, 2.1, '10 Consultas Avançadas | Detecção de Conflitos | Análise Causal', 
            ha='center', fontsize=9)
    
    # Setas
    for y in [7.5, 5.5, 3.5]:
        ax.annotate('', xy=(5, y-0.1), xytext=(5, y+0.1),
                   arrowprops=dict(arrowstyle='->', lw=3, color='black'))
    
    # Outputs
    ax.text(1.5, 0.8, '📄 .ttl files', ha='center', fontsize=10, 
            bbox=dict(boxstyle='round', facecolor='white'))
    ax.text(5, 0.8, '📊 Visualizações', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white'))
    ax.text(8.5, 0.8, '🔍 Análises', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white'))
    
    plt.tight_layout()
    plt.savefig("visualizations/architecture.png", dpi=300, bbox_inches='tight')
    print("✓ Salvo: visualizations/architecture.png")
    plt.close()

def main():
    """Executa todas as visualizações"""
    # Criar diretório
    os.makedirs("visualizations", exist_ok=True)
    
    print("=" * 80)
    print(" GERANDO VISUALIZAÇÕES DA ONTOLOGIA")
    print("=" * 80)
    
    create_class_hierarchy_graph()
    create_interactive_graph()
    create_statistics_chart()
    create_axioms_diagram()
    create_architecture_diagram()
    
    print("\n" + "=" * 80)
    print(" ✅ TODAS AS VISUALIZAÇÕES GERADAS COM SUCESSO!")
    print("=" * 80)
    print("\nArquivos criados em: visualizations/")
    print("  • class_hierarchy.png - Hierarquia de classes")
    print("  • ontology_interactive.html - Grafo interativo")
    print("  • statistics.png - Estatísticas do sistema")
    print("  • axioms_diagram.png - Diagramas dos axiomas")
    print("  • architecture.png - Arquitetura do sistema")

if __name__ == "__main__":
    main()
