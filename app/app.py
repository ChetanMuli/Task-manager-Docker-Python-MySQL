from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Task

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html')

    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))
            hashed = generate_password_hash(password)
            user = User(email=email, password=hashed)
            db.session.add(user)
            db.session.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Invalid credentials', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
        counts = {
            'total': len(tasks),
            'todo': sum(1 for t in tasks if t.status == 'To Do'),
            'inprogress': sum(1 for t in tasks if t.status == 'In Progress'),
            'done': sum(1 for t in tasks if t.status == 'Done'),
        }
        return render_template('dashboard.html', tasks=tasks, counts=counts)

    @app.route('/task/new', methods=['GET','POST'])
    @login_required
    def new_task():
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            task = Task(user_id=current_user.id, title=title, description=description)
            db.session.add(task)
            db.session.commit()
            flash('Task created', 'success')
            return redirect(url_for('dashboard'))
        return render_template('task_form.html', action='Create')

    @app.route('/task/<int:task_id>/edit', methods=['GET','POST'])
    @login_required
    def edit_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash('Not authorized', 'danger')
            return redirect(url_for('dashboard'))
        if request.method == 'POST':
            task.title = request.form.get('title')
            task.description = request.form.get('description')
            task.status = request.form.get('status')
            db.session.commit()
            flash('Task updated', 'success')
            return redirect(url_for('dashboard'))
        return render_template('task_form.html', action='Edit', task=task)

    @app.route('/task/<int:task_id>/delete', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash('Not authorized', 'danger')
            return redirect(url_for('dashboard'))
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted', 'success')
        return redirect(url_for('dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
