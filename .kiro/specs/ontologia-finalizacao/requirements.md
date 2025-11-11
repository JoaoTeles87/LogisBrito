# Requirements Document

## Introduction

Este documento especifica os requisitos para finalizar o projeto LogisBrito, uma ontologia OWL DL para análise de conflitos urbanos em Recife. O projeto já possui um schema de ontologia (v4) e instâncias básicas implementadas. A finalização envolve: implementar inferência lógica usando reasoners OWL, criar consultas SPARQL para extrair narrativas de conflito, desenvolver testes automatizados, e melhorar a documentação existente.

## Glossary

- **Sistema**: O conjunto de notebooks Jupyter, arquivos de ontologia (.ttl), e scripts Python que compõem o LogisBrito
- **Reasoner**: Motor de inferência OWL que deduz novos fatos a partir de regras e dados existentes (owlrl)
- **Base de Conhecimento**: Grafo RDF contendo o schema da ontologia e as instâncias de dados
- **Consulta SPARQL**: Query declarativa para extrair informações específicas do grafo RDF
- **Tripla Inferida**: Fato deduzido pelo reasoner que não estava explicitamente declarado
- **Usuário**: Estudante ou pesquisador que utilizará o sistema para análise de conflitos urbanos

## Requirements

### Requirement 1

**User Story:** Como um pesquisador, eu quero que o sistema execute inferência lógica sobre a base de conhecimento, para que novos fatos sejam deduzidos automaticamente a partir das regras OWL.

#### Acceptance Criteria

1. WHEN o notebook de inferência é executado, THE Sistema SHALL carregar a base de conhecimento existente (kb_conflito_urbano_final.ttl)
2. WHEN o reasoner OWL DL é aplicado, THE Sistema SHALL expandir o grafo com triplas inferidas
3. THE Sistema SHALL salvar o grafo expandido em um novo arquivo (kb_conflito_urbano_inferido.ttl)
4. THE Sistema SHALL exibir a contagem de triplas antes e depois da inferência
5. WHEN a inferência é concluída, THE Sistema SHALL validar que pelo menos uma tripla foi inferida corretamente

### Requirement 2

**User Story:** Como um pesquisador, eu quero executar consultas SPARQL sobre o grafo inferido, para que eu possa extrair narrativas específicas sobre conflitos urbanos.

#### Acceptance Criteria

1. THE Sistema SHALL implementar uma consulta SPARQL que identifica atores executando ações de classes opostas (Propositiva e Impeditiva)
2. THE Sistema SHALL implementar uma consulta SPARQL que rastreia a cadeia de causalidade de danos urbanos
3. THE Sistema SHALL implementar uma consulta SPARQL que identifica instrumentos em conflito direto sobre o mesmo dano
4. WHEN cada consulta é executada, THE Sistema SHALL exibir os resultados em formato legível
5. THE Sistema SHALL executar todas as consultas sobre o grafo inferido (não o original)

### Requirement 3

**User Story:** Como um desenvolvedor, eu quero testes automatizados para a ontologia, para que eu possa validar a integridade do schema e das instâncias.

#### Acceptance Criteria

1. THE Sistema SHALL validar que o arquivo de schema pode ser carregado sem erros de sintaxe
2. THE Sistema SHALL validar que todas as classes principais estão definidas no schema
3. THE Sistema SHALL validar que todas as propriedades de objeto estão corretamente tipadas
4. THE Sistema SHALL validar que as restrições de disjointWith estão presentes
5. THE Sistema SHALL validar que as instâncias estão corretamente tipadas

### Requirement 4

**User Story:** Como um usuário, eu quero documentação clara e completa, para que eu possa entender o propósito, arquitetura e uso do sistema.

#### Acceptance Criteria

1. THE Sistema SHALL fornecer um README atualizado com seções sobre progresso atual e próximos passos
2. THE Sistema SHALL documentar a estrutura da ontologia (classes, propriedades, hierarquias)
3. THE Sistema SHALL fornecer exemplos de uso dos notebooks
4. THE Sistema SHALL documentar os resultados esperados das consultas SPARQL
5. THE Sistema SHALL incluir um guia de instalação e configuração do ambiente

### Requirement 5

**User Story:** Como um pesquisador, eu quero visualizar os resultados das consultas SPARQL, para que eu possa compreender as narrativas de conflito de forma intuitiva.

#### Acceptance Criteria

1. WHEN uma consulta SPARQL retorna resultados, THE Sistema SHALL formatar a saída de forma estruturada
2. THE Sistema SHALL incluir labels legíveis (não apenas URIs) nos resultados
3. THE Sistema SHALL agrupar resultados relacionados logicamente
4. THE Sistema SHALL destacar conflitos lógicos identificados
5. THE Sistema SHALL permitir exportação dos resultados em formato texto
