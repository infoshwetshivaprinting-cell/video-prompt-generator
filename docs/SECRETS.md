# Storing Secrets Securely

This project uses environment variables to keep API keys and credentials out of the repository. Do NOT commit any secret values (API keys, service account JSON files, etc.) to Git.

Recommended patterns

- Local development (.env)
  - Add a file named `.env` to the project root with the variables you need (follow the keys in `.env.example`).
  - Add `.env` to your `.gitignore` (already included).
  - Use `python-dotenv` in development to load variables: `pip install python-dotenv` and `from dotenv import load_dotenv; load_dotenv()` at your app entry-point if desired.

- Streamlit Community Cloud
  - Use the Secrets manager in Streamlit Cloud (Settings → Secrets) to store keys like `ELEVENLABS_API_KEY` or `YT_API_KEY`.
  - In Streamlit code you can access them via `st.secrets["KEY_NAME"]` or as normal environment variables if you prefer.

- GitHub Actions (CI)
  - Add secrets in your repository Settings → Secrets and variables → Actions → New repository secret.
  - Reference them in workflows using `${{ secrets.MY_SECRET }}`.

- Google Cloud or other platform service accounts
  - Upload JSON credential files to a secure location (not in the repo). In CI or on a server, store the path in an environment variable such as `GOOGLE_APPLICATION_CREDENTIALS` and ensure the file is present at that path.

General guidance

- Never store secrets in code, README, or commit history. If you accidentally commit a secret, rotate/change it immediately.
- Use principle of least privilege when creating API keys/service accounts.
- Prefer read-only keys where possible for testing.
