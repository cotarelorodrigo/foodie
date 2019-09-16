from app import app, db
from models import UserModel

db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)