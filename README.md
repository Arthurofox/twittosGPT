This is a fork of https://github.com/RyanLucas3/poasterGPT

link : https://twittos-gpt.streamlit.app/

## Streamlit secrets

Set the OpenAI key in Streamlit Cloud under:

`App settings` -> `Secrets`

Use this exact secret name:

```toml
OPENAI_API_KEY = "sk-proj-your-key-here"
```

Do not commit a real API key to this public repository.

For local testing, copy `.env.example` to `.env` and replace the placeholder with
your real key.
