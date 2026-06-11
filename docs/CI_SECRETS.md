CI secrets and examples (example-only)

The repository CI can use secrets for tests that require credentials. **Do not** store real secrets in the repo. Add them in GitHub repo Settings → Secrets and variables → Actions.

Example: Add these secrets in your repo settings (if needed)
- ELEVENLABS_API_KEY
- ELEVENLABS_VOICE_ID
- GOOGLE_APPLICATION_CREDENTIALS  (or store JSON in an artifact / secret manager)

Example GitHub Actions snippet to access secrets (do NOT commit actual secrets):

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        env:
          ELEVENLABS_API_KEY: ${{ secrets.ELEVENLABS_API_KEY }}
          ELEVENLABS_VOICE_ID: ${{ secrets.ELEVENLABS_VOICE_ID }}
        run: |
          python -m pytest -q

Notes
- If you don't set these secrets, tests that rely on paid providers should skip or default to free providers. Design tests to not require paid APIs.
- Use GitHub Actions secrets to keep credentials out of code.
