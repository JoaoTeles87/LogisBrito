# Implementation Plan

- [x] 1. Configurar ambiente e dependências
  - Usar `uv` para instalar biblioteca `owlrl` para inferência OWL DL no venv
  - Usar `uv` para instalar `pytest` para testes automatizados no venv
  - Atualizar `requirements.txt` com novas dependências (sem especificar versões)
  - _Requirements: 1.1, 3.1_

- [x] 2. Adicionar inferência ao notebook existente



  - [x] 2.1 Adicionar nova célula de inferência em `notebooks/ontologia_conflito.ipynb`


    - Carregar base de conhecimento `kb_conflito_urbano_final.ttl` já gerada
    - Executar reasoner OWL DL usando `owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)`
    - Salvar grafo inferido em `data/kb_conflito_urbano_inferido.ttl`
    - Exibir estatísticas de triplas antes/depois da inferência
    - Validar que pelo menos uma tripla foi inferida (ex: Prefeitura é AgenteUrbano)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 3. Adicionar consultas SPARQL ao notebook existente





  - [x] 3.1 Adicionar célula de consulta 1: Atores Ambíguos


    - Implementar consulta SPARQL que identifica atores executando ações opostas
    - Formatar e exibir resultados de forma legível
    - Adicionar comentários explicativos sobre a consulta
    - _Requirements: 2.1, 2.4, 5.1, 5.2_
  

  - [x] 3.2 Adicionar célula de consulta 2: Causalidade de Danos

    - Implementar consulta SPARQL que rastreia cadeia de causalidade
    - Formatar e exibir resultados de forma legível
    - Adicionar comentários explicativos sobre a consulta
    - _Requirements: 2.2, 2.4, 5.1, 5.2_

  

  - [ ] 3.3 Adicionar célula de consulta 3: Conflito de Instrumentos
    - Implementar consulta SPARQL que identifica instrumentos em conflito
    - Formatar e exibir resultados de forma legível
    - Destacar conflitos lógicos identificados
    - Adicionar comentários explicativos sobre a consulta
    - _Requirements: 2.3, 2.4, 5.1, 5.2, 5.3, 5.4_

- [x] 4. Criar módulos Python reutilizáveis





  - [x] 4.1 Criar diretório `src/` e arquivo `__init__.py`


    - Criar estrutura básica de pacote Python
    - _Requirements: 1.1, 2.1, 3.1_
  
  - [x] 4.2 Implementar módulo `src/sparql_queries.py`


    - Extrair consultas SPARQL do notebook para módulo reutilizável
    - Criar classe `SPARQLQueryEngine` com métodos para cada consulta
    - Implementar método `format_results()` para formatação legível
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 5.1, 5.2_
  
  - [x] 4.3 Implementar módulo `src/validators.py`


    - Criar classe `OntologyValidator` com métodos de validação
    - Implementar validação de sintaxe Turtle
    - Implementar validação de classes esperadas
    - Implementar validação de propriedades de objeto
    - Implementar validação de restrições disjointWith
    - Implementar validação de tipagem de instâncias
    - Implementar método `generate_report()` para relatório completo
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 5. Criar testes automatizados




  - [x] 5.1 Criar diretório `tests/` e arquivo `test_ontologia.py`


    - Criar estrutura básica de testes pytest
    - _Requirements: 3.1_
  
  - [x] 5.2 Implementar testes de validação de schema

    - Testar que schema pode ser carregado sem erros
    - Testar presença de classes principais (AgenteUrbano, AcaoUrbana, etc.)
    - Testar propriedades de objeto (executaAcao, causa_direta, etc.)
    - Testar restrições disjointWith
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  

  - [x] 5.3 Implementar testes de validação de instâncias



    - Testar que KB completa pode ser carregada
    - Testar tipagem de instâncias (Prefeitura é PoderPublico, etc.)
    - Testar relações entre instâncias
    - _Requirements: 3.5_




  
  - [ ] 5.4 Implementar testes de inferência
    - Testar que reasoner infere subclasses corretamente
    - Testar que grafo inferido contém mais triplas que original
    - Testar que tripla esperada (Prefeitura é AgenteUrbano) foi inferida




    - _Requirements: 1.2, 1.5_
  
  - [x] 5.5 Implementar testes de consultas SPARQL

    - Testar que consulta de atores ambíguos retorna Prefeitura
    - Testar que consulta de causalidade retorna cadeias corretas
    - Testar que consulta de conflito identifica instrumentos opostos
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 6. Melhorar documentação





  - [x] 6.1 Atualizar README.md


    - Adicionar seção "Progresso Atual" com status do projeto
    - Adicionar seção "Estrutura do Projeto" explicando organização de arquivos
    - Atualizar "Technology Stack" incluindo owlrl e pytest
    - Adicionar seção "Como Usar" com instruções de execução
    - _Requirements: 4.1, 4.5_
  
  - [x] 6.2 Criar documento docs/ARCHITECTURE.md


    - Documentar estrutura da ontologia (6 eixos: Agentes, Ações, Instrumentos, Espaços, Danos, Benefícios)
    - Documentar hierarquia de classes com diagrama Mermaid
    - Documentar propriedades de objeto e suas restrições (domain/range)
    - Documentar instâncias principais (Prefeitura, Comunidade Coque, etc.)
    - Explicar restrições disjointWith e seu papel na detecção de conflitos
    - _Requirements: 4.2_
  
  - [x] 6.3 Criar documento docs/USAGE_GUIDE.md


    - Documentar instalação de dependências com uv
    - Documentar execução do notebook passo a passo
    - Incluir exemplos de saída esperada para cada célula
    - Documentar interpretação dos resultados das consultas SPARQL
    - Incluir troubleshooting para erros comuns
    - _Requirements: 4.3, 4.4, 4.5_
  


  - [x] 6.4 Criar documento docs/RESULTADOS.md
    - Documentar triplas inferidas pelo reasoner
    - Documentar narrativas extraídas pelas consultas SPARQL
    - Incluir análise dos conflitos identificados
    - Documentar como o sistema detecta ambiguidade do Poder Público
    - _Requirements: 4.4, 5.5_

- [-] 7. Validação final




  - [x] 7.1 Executar notebook completo


    - Executar todas as células de `ontologia_conflito.ipynb` na ordem
    - Verificar que todos os arquivos são gerados corretamente
    - Verificar que visualização HTML é criada
    - _Requirements: 1.1, 2.1, 3.1_
  


  - [x] 7.2 Executar testes pytest

    - Executar `pytest tests/` no venv
    - Verificar que todos os testes passam
    - Gerar relatório de cobertura de testes
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  

  - [ ] 7.3 Verificar resultados das consultas












    - Confirmar que consulta de atores ambíguos identifica Prefeitura
    - Confirmar que consulta de causalidade rastreia gentrificação no Coque
    - Confirmar que consulta de conflito identifica PREZEIS vs Remembramento
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 5.4_

  - [ ] 7.4 Atualizar documentação caso precise
    - Caso haja alguma atualização necessária
    - _Requirements: 4.1, 4.5_

