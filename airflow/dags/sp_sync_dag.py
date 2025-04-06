# airflow/dags/sp_sync_dag.py

from datetime import datetime, timedelta

from sp_api.util import retry

from airflow import DAG
from airflow.operators.bash import BashOperator

#----------------------------------------------------
#Why?
# This Dag Schedules all 3 sync scripts (orders, order_items, sales)
# You can later run them in parallel or add retry alerts as needed.
#----------------------------------------------------

# Default arguments for all tasks in this DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['surypratap0369@gmail.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    dag_id='amazon_order_items_sync',
    default_args=default_args,
    description='Sync data from SP API using Amazon + Sales Scripts',
    schedule_interval=timedelta(days=1), # Change @hourly if needed hourly or dailya as needed
    start_date=datetime(2025, 4, 6),
    catchup=False,
    tags=['sp-api','amazon','sync']
)


# ───────────────────────────────────────
# 🔧 Task 1: Sync Amazon Orders
# ───────────────────────────────────────

sync_orders = BashOperator(
    task_id='sync_amazon_orders',
    bash_command = 'python /app/sales_data/amazon_sync.py',
    dag=dag
)


# ───────────────────────────────────────
# 🔧 Task 2: Sync Order Items
# ───────────────────────────────────────

sync_order_items = BashOperator(
    task_id='sync_order_items',
    bash_command = 'python /app/sales_data/order_items-sync.py',\
    dag=dag
)

# ───────────────────────────────────────
# 🔧 Task 3: Sync Sales Summary
# ───────────────────────────────────────
sync_sales_summary = BashOperator(
    task_id='sync_sales_summary',
    bash_command = 'python /app/sales_data/update_daily_sales.py',
    dag=dag
)

# ───────────────────────────────────────
# 📊 Task Dependencies (sequential)
# Can be made parallel by removing these arrows
# ───────────────────────────────────────
sync_orders >> sync_order_items >> sync_sales_summary
