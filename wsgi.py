import os
from src.app import app, db
from src.models import UserModel

db.create_all()
db.session.commit()

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
