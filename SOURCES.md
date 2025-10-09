# Project Sources

This file tracks the primary sources of data, technical knowledge, and conceptual inspiration for the `Oráculo de Brito` project.

*For a complete and detailed bibliography, including academic papers, news articles, and annotations, please refer to our managed library (link to be added).*

---

### Primary Legal & Urban Data Sources

This is the raw material used to build the project's knowledge base.

* **[Recife - Land Use and Occupation Zoning Plan (Lei de Uso e Ocupação do Solo)](https://leismunicipais.com.br/plano-de-zoneamento-uso-e-ocupacao-do-solo-recife-pe)**
    * **Description:** The primary legal document detailing the urban regulations, zoning, and land use rules for the city of Recife. This is a foundational source for the expert system's rule base.
    * **Usage:** Direct extraction of rules for zones, building heights (`gabarito`), permitted uses, etc.

* **[Cartogram of ZEIS in Recife](https://github.com/SEU_USUARIO/UrbeSegura-Recife/blob/main/data/cartograma-zeis-recife.jpg)**
    * **Description:** A map detailing the location of Special Zones of Social Interest (ZEIS) throughout Recife, along with geographic context (hills, plains, estuary).
    * **Usage:** Used to create instances of ZEIS and link them to their respective neighborhoods and geographical risk areas in the ontology.

---

### Technical Foundation

Articles and tutorials that inform the project's technical architecture.

* **[Introduction to RDF, RDFS, and OWL (in Portuguese)](https://www.linkedin.com/pulse/rdf-rdfs-e-owl-jose-r-f-junior-cpgjf/)**
    * **Description:** An introductory article explaining the core concepts of the Semantic Web stack, including the Resource Description Framework (RDF) and the Web Ontology Language (OWL).
    * **Usage:** Serves as a conceptual guide for the data modeling and ontology construction using `rdflib` in Python.

---

### Conceptual & Ethical Foundation

Academic papers that provide the theoretical and ethical grounding for the project.

* **[arXiv: "Ethical and Social Risks of Harm from Language Models"](https://arxiv.org/abs/2009.14654)**
    * **Description:** A foundational paper detailing the potential risks of large language models, including misinformation, bias, and the difficulty of auditing their behavior.
    * **Usage:** This paper helps frame the "why" of our project, justifying the need for a verifiable, logic-based system as a counterpoint to probabilistic LLMs in high-stakes domains like urban legislation.