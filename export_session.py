import csv, requests, os
API = "http://localhost:8000/admin/export/{session_id}"
API_KEY = os.getenv("ADMIN_API_KEY")
def export(session_id, fname):
    r = requests.get(API.format(session_id=session_id), headers={"api-key": API_KEY})
    r.raise_for_status()
    data = r.json()
    visits = data.get("visits", [])
    with open(fname, "w", newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(["id","session_id","ip","user_agent","timestamp","latitude","longitude","city","region","country"])
        for v in visits:
            w.writerow([v.get("id"), v.get("session_id"), v.get("ip"), v.get("user_agent"), v.get("timestamp"), v.get("latitude"), v.get("longitude"), v.get("city"), v.get("region"), v.get("country")])
    print("Exported:", fname)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python export_session.py <session_id> <output.csv>")
    else:
        export(sys.argv[1], sys.argv[2])
