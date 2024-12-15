# helpers/scheduler.py
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def should_send_report(last_sent, frequency):
    now = datetime.now()
    delta = now - last_sent

    if frequency == "week" and delta.days >= 7:
        return True
    if frequency == "month" and delta.days >= 30:
        return True
    if frequency == "quarter" and delta.days >= 90:
        return True
    if frequency == "year" and delta.days >= 90:
        return True
    return False

def schedule_reports(websites, process_website):
    now = datetime.now()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_website, site, now) for site in websites]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing a website: {e}")
