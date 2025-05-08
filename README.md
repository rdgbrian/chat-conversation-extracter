# 📦 Chat Conversation Extractor

This project provides tools to **extract, preprocess, cluster, and summarize WhatsApp chat conversations** using modern NLP techniques. It supports anonymization of sensitive data and interactive exploration of chat messages.

---

## 🚀 Features

- 📁 **WhatsApp Chat Parser** — convert exported `.txt` chats into structured tabular data
- 🧼 **Anonymization** — hash phone numbers and remove sensitive identifiers
- 🧠 **Topic Modeling** — using BERTopic for unsupervised topic discovery
- 🧪 **Interactive Exploration** — GUI-based message viewer with filtering
- 📊 **Visualization & Summarization** — clustering, topic trends, and summary generation

---

## 🗂 Project Structure

```plaintext
chat-conversation-extracter/
├── anon_data.py                 # Anonymize phone numbers from raw CSVs
├── pyproject.toml              # Build configuration (PEP 517/518)
├── requirements.txt            # Python dependencies
├── setup.py                    # Legacy build script (for compatibility)
├── tree.txt                    # Text output of directory tree
│
├── data/
│   ├── raw/                    # Original chat exports (excluded from Git)
│   │   └── README.md
│   └── tabular/                # Processed CSVs with user_id
│       └── README.md
│
├── notebooks/
│   ├── bert-topic-testing.ipynb     # Topic modeling experiments
│   └── nlp-conversation-demo.ipynb  # Main demo and summarization workflow
│
└── src/
    └── nlp_text_messaging/
        ├── message_cluster.py        # Topic modeling and clustering
        ├── message_gui.py            # Interactive message viewer
        └── preprocess_chat_data.py   # Raw data parsing and cleaning
