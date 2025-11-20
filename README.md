# Multi-Agent Trading Consensus System

> An AI-powered trading decision platform that uses multiple specialized agents to reach consensus through debate and collective intelligence.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

## Important Disclaimer

**This system is for educational and research purposes only. It does NOT provide financial advice. Always conduct your own research and consult with licensed financial advisors before making any trading decisions. Trading involves substantial risk of loss.**

---

## Overview

The **Multi-Agent Trading Consensus System** orchestrates multiple AI agents with different analytical perspectives to generate trading signals through a debate-based consensus mechanism. Instead of relying on a single model, the system leverages collective intelligence to make more robust trading decisions.

### Key Features

- **Multi-Agent Architecture**: 4 specialized AI agents with distinct roles
- **Debate-Based Consensus**: Agents iteratively refine their positions through structured debate
- **Dual Memory System**: Short-term (Redis) and long-term (FAISS vector store) memory
- **RAG Integration**: Retrieval-Augmented Generation for historical context
- **Weighted Decision Making**: Agent opinions are weighted by their expertise
- **RESTful API**: Flask-based HTTP API for easy integration
- **Graceful Degradation**: System continues functioning even if some agents fail

---

## Architecture

### Agent System

| Agent | Model | Role | Weight | Focus |
|-------|-------|------|--------|-------|
| **ChatGPT Agent** | GPT-4 Turbo | Fundamental Analysis | 1.0 | Company financials, earnings, news |
| **Grok Agent** | Grok Beta | Social Sentiment | 1.0 | Social media trends, sentiment analysis |
| **Gemini Agent** | Gemini Pro | Technical Analysis | 1.2 | Chart patterns, indicators, price action |
| **Machine Agent** | Llama 3.1* | Risk & Execution | 1.1 | Risk assessment, position sizing |

*Requires fine-tuned model (currently uses fallback logic)

### System Flow

```
1. Data Acquisition → Market data + news feed
2. Context Retrieval → RAG engine fetches historical patterns
3. Initial Analysis → Each agent analyzes independently
4. Debate Loop → Agents argue and refine positions (max 5 rounds)
5. Consensus Calculation → Weighted voting determines final decision
6. Memory Storage → Experience saved for future reference
```

### Consensus Algorithm

```python
# Weighted consensus formula
for each agent:
    score[signal] += agent_weight × agent_confidence

final_decision = argmax(score)
```

Early exit occurs when consensus confidence ≥ 70%

---

## Quick Start

### Prerequisites

- Python 3.8+
- Redis (optional - falls back to in-memory storage)
- API keys for AI services (see Configuration)

### Installation

```bash
# Clone the repository
git clone https://github.com/esenbora/trading_consensus_system.git
cd trading_consensus_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Create a `.env` file with the following variables:

```env
# Required for ChatGPT Agent
OPENAI_API_KEY=sk-your-openai-key

# Required for Grok Agent
XAI_API_KEY=your-xai-key

# Required for Gemini Agent
GOOGLE_API_KEY=your-google-key

# Optional (uses mock if not configured)
REDIS_HOST=localhost
REDIS_PORT=6379
MACHINE_MODEL_PATH=./models/machine_finetuned.gguf
```

### Running the System

**Option 1: Verification Script (Test Mode)**

```bash
python verification_script.py
```

**Option 2: Flask API Server**

```bash
python app.py
# Server runs on http://localhost:5000
```

**Option 3: API Usage**

```bash
# Check system status
curl http://localhost:5000/status

# Analyze a ticker
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "BTC-USD"}'
```

---

## Example Output

```json
{
  "message": "Analysis completed for BTC-USD",
  "status": "success",
  "consensus": "BUY",
  "confidence": 0.78,
  "details": {
    "ticker": "BTC-USD",
    "rounds": 3,
    "decision": "BUY",
    "confidence": 0.78,
    "history": [
      {
        "agent": "ChatGPT Agent",
        "weight": 1.0,
        "opinion": {
          "signal": "BUY",
          "confidence": 0.75,
          "reasoning": "Strong fundamentals and institutional adoption..."
        }
      }
      // ... more agents
    ],
    "market_data": {
      "ticker": "BTC-USD",
      "price": 45230.50,
      "volume": 28500000000,
      "change_24h": 3.2,
      "rsi": 62
    }
  }
}
```

---

## Current Implementation Status

### Fully Implemented

- Multi-agent orchestration system
- Debate consensus mechanism
- Flask REST API
- Redis client with fallback
- FAISS vector store
- Error handling and graceful degradation
- Configuration management

### Mock Implementations (Require Setup)

**Data Feed** (`data/feed.py`)
- Currently returns simulated market data
- Ready for integration with:
  - Alpha Vantage API
  - Polygon.io
  - Binance API
  - Yahoo Finance

**Embeddings** (`memory/rag_engine.py`)
- Uses placeholder vectors `[0.1] * 768`
- Ready for real embedding models:
  - OpenAI Embeddings
  - Sentence Transformers
  - Cohere Embeddings

**Machine Agent** (`agents/implementations.py`)
- Returns hardcoded logic
- Requires fine-tuned Llama 3.1 model at `models/machine_finetuned.gguf`

**Telegram Notifications** (`utils/telegram_bot.py`)
- Prints to console
- Ready for Telegram Bot API integration

---

## Testing

```bash
# Run verification script
python verification_script.py

# Test specific agent
from agents import ChatGPTAgent
agent = ChatGPTAgent(name="Test", model="gpt-4-turbo", role="Test", weight=1.0, temperature=0.7)
result = agent.analyze({"ticker": "AAPL", "price": 180.5})
print(result)
```

---

## Project Structure

```
trading_consensus_system/
├── agents/                    # AI Agent implementations
│   ├── __init__.py
│   ├── base.py               # Abstract BaseAgent class
│   └── implementations.py    # ChatGPT, Grok, Gemini, Machine agents
│
├── memory/                    # Memory and retrieval systems
│   ├── rag_engine.py         # RAG orchestrator
│   ├── redis_client.py       # Short-term memory
│   └── vector_store.py       # Long-term FAISS store
│
├── data/                      # Market data acquisition
│   └── feed.py               # DataFeed (currently mock)
│
├── utils/                     # Utilities
│   └── telegram_bot.py       # Alert system (currently mock)
│
├── app.py                     # Flask REST API
├── config.py                  # Configuration
├── orchestrator.py            # Main debate orchestration
├── verification_script.py     # Testing script
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## API Endpoints

### `GET /status`
Check system health

**Response:**
```json
{
  "status": "online",
  "system": "Multi-Agent Trading Consensus"
}
```

### `POST /analyze`
Trigger consensus analysis for a ticker

**Request:**
```json
{
  "ticker": "BTC-USD"
}
```

**Response:**
```json
{
  "message": "Analysis completed for BTC-USD",
  "status": "success",
  "consensus": "BUY",
  "confidence": 0.78,
  "details": { /* full debate history */ }
}
```

---

## Configuration Options

Edit `config.py` to customize:

- **Agent Weights**: Adjust influence of each agent
- **Consensus Threshold**: Default 0.70 (70% confidence)
- **Max Debate Rounds**: Default 5 rounds
- **Temperature Settings**: Control randomness per agent
- **Model Names**: Switch between different AI models

---

## Contributing

Contributions and collaborations are welcome! Areas for improvement:

1. Real market data integration
2. Fine-tuned Machine Agent model
3. Improved embedding generation
4. Additional agents (e.g., options flow, on-chain metrics)
5. Backtesting framework
6. UI dashboard
7. Unit tests and integration tests

Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by OpenAI, Google, and xAI models
- Vector search with [FAISS](https://github.com/facebookresearch/faiss)
- Web framework: [Flask](https://flask.palletsprojects.com/)

---

## Contact

For questions, suggestions, or collaboration:
- GitHub Issues: [Open an issue](https://github.com/esenbora/trading_consensus_system/issues)
- Twitter/X: [@esenbora](https://twitter.com/esenbora)

---

## Quick Tips

1. **Start with mock data**: Test the system without API keys to understand the flow
2. **API costs**: Be aware of API usage costs, especially for GPT-4 and Gemini
3. **Redis optional**: System works without Redis using in-memory fallback
4. **Model selection**: You can use cheaper models (gpt-3.5-turbo) for testing
5. **Rate limiting**: Implement rate limiting for production use

---

**Remember: Past performance does not guarantee future results. This is an experimental system for educational purposes only.**
