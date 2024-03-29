from tbcompanion import create_app
from tbcompanion import db

app = create_app()

with app.test_request_context():
	db.create_all()	

app.app_context().push()

if __name__ == '__main__':
	app.run(debug=True)
