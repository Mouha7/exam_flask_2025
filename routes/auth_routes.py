from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from services.auth_service import register_user, authenticate_user, logout

def register_auth_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            success, message = register_user(username, email, password)
            
            if success:
                flash(message, 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'danger')
        
        return render_template('auth/register.html', title='Inscription')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            remember = 'remember' in request.form
            
            success, message = authenticate_user(username, password, remember)
            
            if success:
                next_page = request.args.get('next')
                flash(message, 'success')
                return redirect(next_page or url_for('home'))
            else:
                flash(message, 'danger')
        
        return render_template('auth/login.html', title='Connexion')
    
    @app.route('/logout')
    @login_required
    def logout_route():
        logout()
        flash('Vous avez été déconnecté.', 'info')
        return redirect(url_for('home'))