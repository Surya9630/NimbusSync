# 🧪 Command Reference Sheet

## ⚙️ Docker & Docker Compose

| Task | Command |
|------|---------|
| Start containers in detached mode | `docker-compose up -d` |
| Stop & remove containers, networks | `docker-compose down` |
| Rebuild images without cache | `docker-compose build --no-cache` |
| View container logs | `docker-compose logs -f <service>` |
| Access container shell | `docker-compose exec <service> bash` |
| Show running containers | `docker ps` |
| Remove orphan containers | `docker-compose up -d --remove-orphans` |

## 🐍 Running Python Scripts (Inside Containers)

```bash
docker-compose exec gorilla_app bash
python sales_data/amazon_sync.py
python sales_data/order_items_sync.py
python sales_data/update_daily_sales.py
```

## 🌬️ Apache Airflow

| Task | Command |
|------|---------|
| List all DAGs | `airflow dags list` |
| Trigger DAG | `airflow dags trigger <dag_id>` |
| Check DAG status | `airflow dags list-runs -d <dag_id>` |
| View task logs | `airflow tasks logs <dag_id> <task_id> <run_id>` |

## 🐙 Git

| Task | Command |
|------|---------|
| Init repo | `git init` |
| Add files | `git add .` |
| Commit | `git commit -m "message"` |
| View log | `git log` |
| Create remote | `git remote add origin <repo_url>` |
| Push to GitHub | `git push -u origin main` |