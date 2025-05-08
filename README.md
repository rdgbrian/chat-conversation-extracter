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
```

---

## 🛠 Setup

### ✅ Install dependencies

```bash
pip install -e .
```

Make sure you are using a virtual environment (e.g. `venv`, `conda`, or `poetry`) to avoid polluting system packages.

---

## 🔐 Data Notice

Raw chat data (e.g., `.txt`, `.csv` exports from WhatsApp) is **excluded from this repository** for privacy reasons. The `/data/raw` and `/data/tabular` folders are used during local development only.

> See `data/raw/README.md` and `data/tabular/README.md` for more information on expected formats and usage.

---

## 📈 Demo Notebooks

- `notebooks/nlp-conversation-demo.ipynb`: End-to-end pipeline with preprocessing, clustering, and summarization
- `notebooks/bert-topic-testing.ipynb`: Testing BERTopic configurations on message sets

---

## 📝 License

This project is distributed for academic and educational purposes. Please respect privacy concerns when working with real messaging data.

---

## 🙋‍♂️ Questions or Contributions?

Feel free to open issues or pull requests. Feedback is welcome!

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
