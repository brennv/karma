from graph_app import app
import os

app.debug = True
app.secret_key = os.urandom(24)
port = int(os.environ.get('PORT', 8000))
app.run(host='0.0.0.0', port=port)
