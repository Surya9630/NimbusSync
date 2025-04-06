## 🔧 Problem: Airflow DAG not importing `sp_api`
**Error:**
`ModuleNotFoundError: No module named 'sp_api'`

**Fix:**
- Add `sp-api==0.8.0` to requirements.txt
- Rebuild docker: `docker-compose build --no-cache`
- Restart: `docker-compose up -d`
