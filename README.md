# News Research Crew 📰

A multi-agent AI system for **unbiased news analysis** powered by [crewAI](https://crewai.com). This project uses 6 specialized AI agents to collect, analyze, detect bias, and generate balanced news digests from multiple sources.

## 🎯 Features

- **Multi-Source News Collection**: Integrates NewsAPI, GDELT, and MediaStack for comprehensive coverage
- **Bias Detection**: Analyzes sentiment, tone, political leaning, and loaded language
- **Stance Equalization**: Transforms biased content into neutral, balanced reporting
- **Multi-Agent Collaboration**: 6 specialized agents working together:
  - Storage Agent (caching & retrieval)
  - Collector Agent (multi-API news fetching)
  - Summarizer Agent (factual extraction)
  - Bias Detector Agent (sentiment & bias analysis)
  - Stance Equalizer Agent (neutralization)
  - Reporter Agent (final digest generation)
- **Flask Web Interface**: User-friendly web app for running analyses and viewing results
- **SQLite Storage**: Local caching to reduce redundant API calls

## 🚀 Installation

### Prerequisites
- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) for dependency management

### Setup

1. **Install UV** (if not already installed):
```bash
pip install uv
```

2. **Clone the repository**:
```bash
git clone https://github.com/anshKjha10/News-Research-Crew.git
cd News-Research-Crew
```

3. **Install dependencies**:
```bash
uv add flask markdown
uv add "crewai[google-genai]"
uv pip install -e .
```

4. **Configure API Keys** - Create/update `.env` file:
```env
# Google Gemini (for LLM)
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here

# GitHub Models (for embeddings/memory)
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_github_token_here
OPENAI_API_BASE=https://models.inference.ai.azure.com

# News APIs
NEWS_API_KEY=your_newsapi_key_here
MEDIASTACK_API_KEY=your_mediastack_key_here

# Model Configuration
MODEL=gemini/gemini-2.0-flash-exp
```

**Get API Keys:**
- Google Gemini: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- GitHub Token: [https://github.com/settings/tokens](https://github.com/settings/tokens)
- NewsAPI: [https://newsapi.org/](https://newsapi.org/)
- MediaStack: [https://mediastack.com/](https://mediastack.com/)

## 📖 Usage

### Option 1: Flask Web Interface (Recommended)

1. **Start the Flask app**:
```bash
python app.py
```

2. **Open browser**:
```
http://localhost:5000
```

3. **Use the interface**:
   - Enter a news topic (e.g., "artificial intelligence")
   - Optionally add a refined query for focused analysis
   - Click "Run Analysis"
   - Download or view the generated markdown report

### Option 2: Command Line

```bash
# Set environment variables
$env:TOPIC="artificial intelligence"
$env:REFINED_QUERY=""  # Leave empty for comprehensive analysis
$env:CURRENT_YEAR="2025"

# Run the crew
crewai run
```

## 🏗️ Project Structure

```
news_research_crew/
├── src/news_research_crew/
│   ├── config/
│   │   ├── agents.yaml          # Agent definitions
│   │   └── tasks.yaml           # Task configurations
│   ├── tools/
│   │   ├── custom_tool.py       # CrewAI tool wrappers
│   │   ├── news_fetcher.py      # Multi-API news fetching
│   │   ├── news_store.py        # SQLite storage
│   │   └── simple_cache.py      # JSON caching
│   ├── crew.py                  # Agent orchestration
│   └── main.py                  # CLI entry point
├── templates/                   # Flask HTML templates
│   ├── index.html              # Main form
│   ├── results.html            # Results list
│   └── view_result.html        # Individual result
├── app.py                       # Flask web application
├── pyproject.toml              # Dependencies
└── .env                        # API keys (create this)
```

## 🤖 How It Works

1. **Storage Agent** checks for cached news articles
2. **Collector Agent** fetches from NewsAPI, GDELT, MediaStack (if cache miss)
3. **Storage Agent** persists collected articles in SQLite
4. **Summarizer Agent** extracts key facts and verifiable information
5. **Bias Detector Agent** analyzes sentiment, tone, and political bias
6. **Stance Equalizer Agent** rewrites content in neutral language
7. **Reporter Agent** generates final balanced news digest

## 📊 Output Format

The final report includes:
- 📊 Executive Summary
- 🔑 Key Facts (location, date, impact, status)
- 📰 The Story (what, why, what's next)
- 🗣️ Multiple Perspectives (government, communities, experts, international)
- 🌍 Broader Context
- 📚 Sources

## 🛠️ Technologies

- **CrewAI 1.2.1**: Multi-agent orchestration
- **Google Gemini 2.0**: LLM for agent reasoning
- **Flask**: Web interface
- **NewsAPI, GDELT, MediaStack**: News sources
- **SQLite**: Local storage
- **httpx**: Async API calls
- **python-dotenv**: Environment management

## 📝 Customization

- **Modify agents**: Edit `src/news_research_crew/config/agents.yaml`
- **Modify tasks**: Edit `src/news_research_crew/config/tasks.yaml`
- **Add tools**: Update `src/news_research_crew/tools/custom_tool.py`
- **Change workflow**: Modify `src/news_research_crew/crew.py`

## 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
uv add flask markdown
```

**Issue**: `Google Gen AI native provider not available`
```bash
uv add "crewai[google-genai]"
```

**Issue**: `OPENAI_API_KEY environment variable is not set`
- Add GitHub token as `OPENAI_API_KEY` in `.env` file (used for embeddings)

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Ansh Kumar Jha**
- GitHub: [@anshKjha10](https://github.com/anshKjha10)
- LinkedIn: [anshkjha10](https://www.linkedin.com/in/anshkjha10)

## 🙏 Support

For questions or feedback:
- Open an issue on [GitHub](https://github.com/anshKjha10/News-Research-Crew)
- CrewAI Documentation: [https://docs.crewai.com](https://docs.crewai.com)

---

**Built with ❤️ using CrewAI**
