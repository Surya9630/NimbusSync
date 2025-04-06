# ❌ Errors and Fixes Log — NimbusSync

This document tracks all major issues, mistakes, and their corresponding fixes throughout the NimbusSync project journey.

---

## ✅ Airflow Errors

### 1. `Broken DAG: No module named 'sp_api'`
- **Reason**: Required module `sp_api` not installed inside Airflow container.
- **Fix**: 
  - Add `sp_api` to `requirements.txt`.
  - Rebuild Airflow image with `docker-compose build --no-cache`.

### 2. `You need to initialize the database. Please run airflow db init`
- **Reason**: Airflow DB was not initialized on first run.
- **Fix**: 
  - Run `docker-compose exec airflow_webserver airflow db init`.

---

## 🐳 Docker Mistakes

### 1. `COPY dags/ /opt/airflow/dags` fails
- **Reason**: Local `dags/` folder didn't exist at the time of build.
- **Fix**: Create the directory using:
  ```bash
  mkdir -p airflow/dags airflow/plugins
  ```

### 2. Volume vs Build Confusion
- **Problem**: Adding modules via `requirements.txt` didn't reflect inside Airflow container.
- **Fix**: Ensure Dockerfile installs requirements and **bind volumes only for DAGs/logs/plugins**, not whole repo.

---

## 🐍 Python Mistakes

### 1. Running pip as root in Dockerfile
- **Error**: 
  ```
  You are running pip as root. Please use 'airflow' user to run pip!
  ```
- **Fix**:
  Use:
  ```Dockerfile
  USER airflow
  RUN pip install --no-cache-dir -r /requirements.txt
  ```

### 2. `psycopg2.OperationalError: could not translate host name 'db'`
- **Reason**: Hostname `db` wasn’t recognized.
- **Fix**: Ensure the service is named `db` in docker-compose and both containers are in the same network.

---

## 💡 Tips

- Always use `docker-compose down` before a `--no-cache` build to clear networks and rebuild correctly.
- Check logs with:
  ```bash
  docker-compose logs -f airflow_webserver
  docker-compose logs -f airflow_scheduler
  ```

