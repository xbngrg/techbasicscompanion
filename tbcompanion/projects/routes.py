from flask import Blueprint, render_template, url_for, current_app
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from tbcompanion import db
from tbcompanion.projects.forms import ProjectForm
from tbcompanion.models import Project, User
from werkzeug.utils import redirect
from tbcompanion.config import Config
from github import Github
import io

projects = Blueprint('projects', __name__)
g = Github(
	client_id = Config.CLIENT_ID,
	client_secret = Config.CLIENT_SECRET)


@projects.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
	project = Project.query.get_or_404(project_id)
	github_user = g.get_user('GiorginoSerbuciano')
	github_project_repo = github_user.get_repo('techbasicscompanion')
	github_project_readme = github_project_repo.get_contents("README.md")
	github_project_readme_str = github_project_readme.decoded_content.decode()
	# with open(r'tbcompanion\accounts\readme.md', 'wb') as readme:
	#	readme.write(github_project_readme.decoded_content)


	return render_template(
		'project_view.html',
		title=project.title,
		project=project,
		readme=github_project_readme_str)


@projects.route('/project/new', methods=['GET', 'POST'])
@login_required
def project_form():
	form = ProjectForm()
	tags = form.dropdown_tags
	if form.validate_on_submit():
		form_data_contributors = form.contributors.data.split(', ')
		project_contributors = []
		if form_data_contributors[0] == '':
			project_contributors.insert(0, current_user)
		else:
			for c in range(len(form_data_contributors)):
				contributor = User.query.filter_by(username=form_data_contributors[c]).first()
				project_contributors.append(contributor)
				project_contributors.insert(0, current_user)
		project = Project(
			title=form.title.data,
			content=form.content.data,
			admin=current_user,
			contributors=project_contributors,  # wants User objects
			github_repo=form.github_repo.data,
			tag=form.tag.data
		)
		db.session.add(project)
		db.session.commit()
		flash('Your project is live!', 'success')
		return redirect(url_for('main.home'))
	return render_template('project_form.html', form=form, type='project', tags=tags)
