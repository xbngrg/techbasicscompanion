from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods = ['GET', 'POST'])
def admin():
	return render_template('admin.html')