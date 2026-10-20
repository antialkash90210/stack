import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": "db",
    "port": 5432,
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "dbname": os.environ["POSTGRES_DB"],
    "connect_timeout": 3,
}


def check_db():
    """Возвращает True, если БД доступна, иначе False."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return True
    except Exception:
        return False


@app.route("/")
def index():
    return jsonify({"message": "Hello from Flask", "status": "ok"})


@app.route("/health")
def health():
    if check_db():
        return jsonify({"status": "healthy", "database": "up"}), 200
    return jsonify({"status": "unhealthy", "database": "down"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response
import time

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['endpoint'])

@app.before_request
def start_timer():
    from flask import g
    g.start = time.time()

@app.after_request
def record_metrics(response):
    from flask import g, request
    if request.path != '/metrics':
        latency = time.time() - g.start
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, status=response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
