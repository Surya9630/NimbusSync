# NimbusSync ☁️📦

**NimbusSync** is a modular, Dockerized data orchestration platform designed to sync and process Amazon SP-API data with Airflow. The name **Nimbus** refers to a cloud, aligning with modern cloud-based data infrastructures, and **Sync** captures the project’s core functionality: synchronizing e-commerce data reliably and repeatedly.

---

## 📌 Project Objective

To create a robust, modular, and extensible platform that:
- Pulls and stores **Amazon SP-API data** (orders, order items, summaries)
- Schedules and automates these sync jobs using **Apache Airflow**
- Logs operations and errors for easy monitoring
- Uses Docker for environment consistency and portability
- Is production-ready and GitHub-presentable

---

## 📁 Folder Structure

```
NimbusSync/
├── airflow/
│   ├── dags/                  # Airflow DAGs for scheduling sync
│   ├── logs/                  # Airflow execution logs
│   └── plugins/               # Custom Airflow plugins (if any)
├── db/
│   ├── connect.py             # SQLAlchemy DB engine setup
│   └── models.py              # PostgreSQL table definitions
├── sales_data/
│   ├── amazon_sync.py         # Full historical Amazon order sync
│   ├── order_items_sync.py    # Sync order item-level data
│   ├── fetch_historic_sales.py
│   └── update_daily_sales.py  # Daily incremental update script
├── utils/
│   ├── logger.py              # Logger setup
│   └── monitor.py             # Post-sync data validation checker
├── docs/
│   ├── errors-and-fixes.md    # All problems faced and how we solved them
│   └── command-cheatsheet.md  # Docker, Airflow, and Python CLI command reference
├── .env
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.airflow
├── README.md
└── run_all.py
```

---

## ⚙️ Technologies Used

- **Python 3.9** for all sync logic and SP-API integration
- **Amazon Selling Partner API (SP-API)** for data extraction
- **PostgreSQL** for data persistence
- **SQLAlchemy ORM** for DB interaction
- **Apache Airflow 2.7.2** for orchestration
- **Docker** for reproducibility across machines

---
## 🧪 How to Run Locally

```bash
# 1. Clone repo & move in
git clone <repo_url>
cd amazon-sync-engine

# 2. Start Docker containers
docker-compose up --build -d

# 3. Access Airflow UI
http://localhost:8080 (username: airflow, password: airflow)

# 4. Enable + trigger DAGs
```
## ✅ Progress and Phases

| Phase                  | Goal | Status |
|------------------------|------|--------|
| 1. Local MVP           | Docker + PostgreSQL + Sync scripts working | ✅ Done |
| 2. Airflow Integration | DAGs setup and working in UI | ✅ Done |
| 3. Retry + Monitoring  | Add retry + monitor failed inserts | ⬜ Pending |
| 4. Forecasting         | Add Prophet to forecast sales | ⬜ Planned |
| 5. Dashboarding        | Streamlit or FastAPI dashboard | ⬜ Planned |
| 6. Cloud Deployment    | Host with Cloud Run + Cloud SQL | ⬜ Planned |

---

## 🔐 Author & Credits

Made with ❤️ by **Surya** — built from scratch with strong attention to modularity, education, and documentation.

---

For full error logs and how issues were fixed, see [`docs/errors-and-fixes.md`](docs/errors-and-fixes.md)  
For Docker/Airflow/Python commands, see [`docs/command-cheatsheet.md`](docs/command-cheatsheet.md)
