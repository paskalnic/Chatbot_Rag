# 🤖 CV Screener : Chatbot RAG Python

![CI](https://github.com/paskalnic/Chatbot_Rag/actions/workflows/python-app.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.3-green)
![License](https://img.shields.io/badge/license-MIT-blue)

Pipeline RAG (Retrieval-Augmented Generation) end-to-end permettant d'interroger un corpus de CVs en langage naturel. Posez des questions sur vos candidats et obtenez des réponses sourcées avec les extraits exacts des CVs utilisés.

---

## 🚀 Lancer le projet en 3 commandes

```bash
git clone https://github.com/paskalnic/Chatbot_Rag.git
cd Chatbot_Rag
pip install poetry && poetry install
```

Ajoutez vos CVs dans `data/raw/`, puis :

```bash
make ingest   # indexe les CVs dans ChromaDB
make run      # lance l'interface Streamlit
```

---

## 🏗️ Architecture

```
CVs PDF (data/raw/)
        │
        ▼
┌───────────────────┐
│    ingest.py      │  Chargement → Chunking → Embeddings → ChromaDB
│  Pipeline ETL     │  RecursiveCharacterTextSplitter (chunk_size=500)
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   ChromaDB        │  Base vectorielle persistante sur disque
│  (data/chroma_db) │  Embeddings : paraphrase-multilingual-MiniLM-L12-v2
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  retriever.py     │  Recherche sémantique (top_k=5)
└───────────────────┘
        │
        ▼
┌───────────────────┐
│    chain.py       │  Prompt custom + LLM Ollama/Mistral
└───────────────────┘
        │
        ▼
┌───────────────────┐
│     app.py        │  Interface Streamlit avec affichage des sources
└───────────────────┘
```

---

## 🛠️ Stack technique

| Composant | Technologie | Rôle |
|-----------|------------|------|
| Ingestion | LangChain + PyPDF | Chargement et parsing des PDFs |
| Chunking | RecursiveCharacterTextSplitter | Découpage intelligent du texte |
| Embeddings | HuggingFace (multilingue) | Transformation texte → vecteurs |
| Vectorstore | ChromaDB | Stockage et recherche vectorielle |
| LLM | Ollama / Mistral | Génération des réponses |
| Interface | Streamlit | Chat UI avec historique |
| Pipeline | Click + Makefile | CLI configurable |
| Qualité | Ruff + Pytest | Linting et tests unitaires |
| CI/CD | GitHub Actions | Tests automatiques à chaque push |

---

## 📁 Structure du projet

```
chatbot-rag/
├── data/
│   ├── raw/              # CVs sources (PDF) : ajoutez vos CVs ici
│   ├── processed/        # Réservé pour preprocessing futur
│   └── chroma_db/        # Base vectorielle persistante (générée par make ingest)
├── src/
│   ├── ingest.py         # Pipeline d'ingestion configurable
│   ├── retriever.py      # Chargement du retriever
│   ├── chain.py          # Chaîne RAG (LLM + prompt + retriever)
│   └── app.py            # Interface Streamlit
├── tests/
│   └── test_ingest.py    # Tests unitaires
├── .github/workflows/
│   └── python-app.yml    # CI GitHub Actions
├── config.yaml           # Paramètres centralisés
├── Makefile              # Commandes one-liner
└── pyproject.toml        # Dépendances Poetry
```

---

## 🔑 Variables d'environnement

Copie le fichier example et remplis tes valeurs :

```bash
cp .env.example .env
```

```bash
# Si tu utilises OpenAI à la place d'Ollama :
# OPENAI_API_KEY=sk-...

# Chemins (valeurs par défaut)
CONFIG_PATH=config.yaml
CHROMA_PERSIST_DIR=./data/chroma_db
LOG_LEVEL=INFO
```

---

## ⚙️ Configuration

Tous les paramètres sont centralisés dans `config.yaml` :

```yaml
chunking:
  chunk_size: 500       # Taille des chunks en tokens
  chunk_overlap: 50     # Chevauchement pour préserver le contexte

retrieval:
  top_k: 5             # Nombre de chunks récupérés par question

llm:
  model: "mistral"     # Modèle Ollama (local, gratuit, confidentiel)
  temperature: 0.0     # 0 = réponses factuelles, pas créatives
```

---

## 🔒 Choix techniques

**Pourquoi HuggingFace pour les embeddings et pas OpenAI ?**
Les CVs contiennent des données personnelles sensibles. Le modèle `paraphrase-multilingual-MiniLM-L12-v2` tourne entièrement en local : aucune donnée ne quitte la machine.

**Pourquoi Ollama/Mistral et pas GPT ?**
Même logique de confidentialité. L'architecture permet de switcher vers OpenAI en une ligne dans `config.yaml` si le contexte le permet.

**Pourquoi RAG et pas fine-tuning ?**
Le fine-tuning modifie les poids du modèle : coûteux et à recommencer à chaque mise à jour. Le RAG injecte le contexte à la volée : ajouter un CV = `make ingest`, c'est tout.

---

## 🧪 Tests et qualité

```bash
make test    # Lance pytest avec coverage
make lint    # Lance ruff (linting + style)
```

Tests unitaires sur les composants critiques du pipeline :
- `test_load_config` : chargement et parsing de la config
- `test_load_config_file_not_found` : gestion des erreurs
- `test_chunk_documents` : validation du chunking

---

## 📋 Prérequis

- Python 3.12+
- Poetry
- [Ollama](https://ollama.com) avec le modèle Mistral : `ollama pull mistral`

---

## 📄 Licence

MIT : voir [LICENSE](LICENSE)

---

## 👤 Auteur

**Paskal Nicolas** : Data Engineer IA | Python | LLM & RAG

*"Chatbot RAG end-to-end : Pipeline d'ingestion de CVs avec LangChain, ChromaDB, Ollama/Mistral. Embeddings multilingues HuggingFace, interface Streamlit avec affichage des sources. Tests unitaires + CI/CD GitHub Actions."*
