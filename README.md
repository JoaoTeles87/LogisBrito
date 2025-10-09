# LogisBrito: A Logical Oracle for Recife's Urban Legislation

**Project Status:** Initial Research & Development | University Project (CIN-UFPE)

## About the Project

`LogisBrito` is a proof-of-concept expert system designed to serve as a **decision-support tool for urban and social policy** in Recife, Brazil. Named after the visionary urbanist Saturnino de Brito, this project aims to create a logical and auditable knowledge base from the city's complex web of urban legislation.

Our primary goal is to address critical urban challenges, such as the requalification of at-risk social housing zones (ZEIS) and the sustainable regeneration of underutilized historical areas, like the Santo Antônio neighborhood.

## The Core Problem

Recife's urban development is governed by layers of historical master plans, decrees, and preservation laws. This legal framework is complex, often contradictory, and inaccessible to citizens, architects, and even technical staff. Answering a seemingly simple question like "What incentives are available to sustainably retrofit this specific historical building for social housing?" can require weeks of legal research.

Probabilistic models like LLMs are ill-suited for this domain, as they cannot guarantee factual accuracy, provide auditable reasoning, or detect logical conflicts within the legal code—risks that are unacceptable when dealing with legal compliance and public policy.

## Our Approach: Logic over LLMs

This project takes a **symbolic AI** approach, building a knowledge graph based on the **Web Ontology Language (OWL DL)**.

Instead of generating probable text, our system:
1.  **Represents** urban laws as a set of precise, logical facts and rules.
2.  **Uses** a reasoner to make logical deductions based on this knowledge.
3.  **Provides** answers that are fully auditable, tracing every conclusion back to the specific article of law it originated from.
4.  **Enables** "what-if" policy simulations, allowing users to see the logical impact of introducing a new rule or incentive.

This makes the `LogisBrito` a **verifiable oracle**, not a conversational generator.

## Technology Stack

* **Language:** Python
* **Knowledge Representation:** `rdflib` for building the RDF graph and modeling the OWL ontology.
* **Query Language:** SPARQL for querying the knowledge base.
* **Prototyping:** JupyterLab
