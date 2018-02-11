import os
from app import app

app.secret_key = os.urandom(12)
app.run(host = "0.0.0.0", debug=True, threaded = True)
