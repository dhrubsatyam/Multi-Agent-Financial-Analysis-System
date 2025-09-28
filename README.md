
# Multi-Agent-Financial-Analysis-System
This project is a part of AAI520 final team project and a part of Team 6's submission attempt.

## How to Run

1. **Clone the repository** (if you haven't already):
	```bash
	git clone <repo-url>
	cd Multi-Agent-Financial-Analysis-System
	```

2. **Install dependencies** (preferably in a virtual environment):
	```bash
	pip install -r requirements.txt
	```

3. **Set up your environment variables:**
	- Copy `.env.example` to `.env`:
	  ```bash
	  cp .env.example .env
	  ```
	- Edit `.env` and add your API keys:
	  ```env
	  NEWS_API_KEY=your_newsapi_key_here
	  OPENAI_API_KEY=your_openai_key_here
	  ```
	- Both keys are required for full functionality. The app will warn you if any are missing.

4. **Run the Streamlit app:**
	```bash
	streamlit run investment_agent.py
	```

5. **Open the app in your browser:**
	- Streamlit will provide a local URL (usually http://localhost:8501) after starting.

## .env File Format

Your `.env` file should look like this:

```env
NEWS_API_KEY=your_newsapi_key_here
OPENAI_API_KEY=your_openai_key_here
```

**Do not share your .env file or API keys publicly.**
