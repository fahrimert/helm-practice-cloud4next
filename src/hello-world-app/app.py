import logging
from flask import Flask

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

@app.route("/")
def hello():
    logger.info("Hello isteği başarıyla karşılandı.")
    return "Hello World! Pipeline Test Ediliyor - V5"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)