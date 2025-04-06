# 🚀 NimbusSync – Modular Amazon SP-API Sync with Airflow

[![GitHub last commit](https://img.shields.io/github/last-commit/Surya9630/NimbusSync?style=flat-square)](https://github.com/Surya9630/NimbusSync)
[![GitHub stars](https://img.shields.io/github/stars/Surya9630/NimbusSync?style=social)](https://github.com/Surya9630/NimbusSync/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Surya9630/NimbusSync?style=flat-square)](https://github.com/Surya9630/NimbusSync/issues)

---

### 🌩️ What's "NimbusSync"?

> *"Nimbus"* means a **cloud** — and this project reflects the mission of cloud-based, modular syncing of **Amazon Seller data** using SP-API.  
> It’s built to **scale**, **modularize**, and eventually **automate** Amazon order and item syncs for business intelligence and decision making.

---

## 🎯 Project Goal

Build a modular data engineering pipeline that:
- Pulls **Amazon orders and order items** using the SP-API
- Syncs it into **PostgreSQL**
- Uses **Apache Airflow** for scheduling & retry logic
- Includes **timezone-aware daily summaries**
- Can later be connected to a BI dashboard or ML models

---

## 🔧 Technologies Used

- 🐍 Python 3.9 (inside Docker)
- 🛒 Amazon SP-API (Selling Partner API)
- 🌬️ Apache Airflow 2.7.2 (DAGs + BashOperators)
- 🐘 PostgreSQL 13
- 🐳 Docker + Docker Compose
- 📚 SQLAlchemy + Pandas
- 📁 Modular File & Folder Structure

---

## 📁 Folder Structure

```bash
NimbusSync/
├── airflow/                  # Airflow DAGs, logs, plugins
│   ├── dags/
│   ├── logs/
│   └── plugins/
├── db/                       # SQLAlchemy DB models & connectors
├── sales_data/               # Order, OrderItem, Summary sync scripts
├── utils/                    # Logger, monitor, etc.
├── docs/                     # Error logs, setup notes
├── scripts/                  # Extra operational scripts (optional)
├── .env                      # Environment variables (gitignored)
├── .gitignore                # Exclude sensitive & build files
├── docker-compose.yml        # All services defined here
├── Dockerfile, Dockerfile.airflow
├── main.py                   # Optional CLI or sync entrypoint
├── README.md, command_cheatsheet.md, requirements.txt
└── run_all.py                # Trigger all syncs sequentially
```

---

## ✅ Features So Far

- ✅ Full historical sync of Amazon Orders → PostgreSQL  
- ✅ Order Item sync with batch processing + retry logic  
- ✅ Daily Sales Summary sync with **timezone support**  
- ✅ Airflow DAG (`amazon_order_items_sync`) built & deployed  
- ✅ Dockerized setup — build once, run anywhere

---

## 🔜 Roadmap

- [ ] 📅 Add Airflow DAGs for `order` and `sales_summary` syncs
- [ ] 🔄 Airflow scheduling with proper time windows
- [ ] 🧪 Add test coverage
- [ ] 📈 Export data to Google Sheets / Streamlit
- [ ] ☁️ Deploy to GCP Cloud Run + Cloud SQL

---

## 🔐 Author & Credits

Made with ❤️ by **Surya**

[GitHub](https://github.com/Surya9630) | [LinkedIn](https://www.linkedin.com/in/surya-chauhan-933938218/)

---

> This is just the beginning of NimbusSync.  
> Stay tuned for streaming syncs, anomaly detection, and sales forecasting! 🌩️