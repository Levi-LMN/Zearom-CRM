
# ============================================================================
# run.py
# ============================================================================

from app import create_app
from app.auth import init_oauth

app = create_app()
init_oauth(app)

if __name__ == '__main__':
    app.run(debug=True)
