import subprocess

scripts = [
    "sales_data/fetch_historic_sales.py",
    "sales_data/amazon_sync.py",
    "sales_data/order_items_sync.py"
]

for script in scripts:
    print(f"\n🟡 Running {script}...\n" + "-" * 40)
    result = subprocess.run(["python", script], capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(f"🔴 Error in {script}:\n{result.stderr}")
