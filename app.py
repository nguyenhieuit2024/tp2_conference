from backend.config import init_app, db
from backend.conference_routes import conference_bp

app = init_app()
app.register_blueprint(conference_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
