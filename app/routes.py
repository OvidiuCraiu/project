from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Contract
from .forms import LoginForm, RegistrationForm, ContractForm, SearchForm
from .forms import ContractCreationForm
from . import db
import os
from flask import send_file
from .pdf_generator import generate_contract_pdf

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/')
def index():
    return render_template('base.html')


@main.route('/dashboard')
@login_required
def dashboard():
    contracts = current_user.contracts
    contracts = Contract.query.all()
    return render_template('dashboard.html', contracts=contracts)


@main.route('/create_contract', methods=['GET', 'POST'])
@login_required
def create_contract():
    form = ContractCreationForm()
    if form.validate_on_submit():
        contract = Contract(
            title=form.title.data,
            party_one=form.party_one.data,
            party_two=form.party_two.data,
            terms=form.terms.data,
            author=current_user
        )
        db.session.add(contract)
        db.session.commit()
        flash('Contract created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('create_contract.html', form=form)


@main.route('/edit_contract/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contract(id):
    contract = Contract.query.get_or_404(id)
    if contract.author != current_user:
        flash('You do not have permission to edit this contract.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = ContractForm()
    if form.validate_on_submit():
        contract.title = form.title.data
        contract.content = form.content.data
        db.session.commit()
        flash('Contract updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.title.data = contract.title
        form.content.data = contract.content
    return render_template('edit_contract.html', form=form, contract=contract)


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search_contracts():
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search.data
        contracts = Contract.query.filter(
            Contract.title.contains(search_term) | Contract.content.contains(search_term)).all()
        return render_template('search_contracts.html', contracts=contracts, form=form)
    return render_template('search_contracts.html', form=form)

@main.route('/export_contract/<int:id>')
@login_required
def export_contract(id):
    contract = Contract.query.get_or_404(id)
    if contract.author != current_user:
        flash('You do not have permission to export this contract.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    filename = f"contract_{contract.id}.pdf"
    filepath = os.path.join(app.instance_path, filename)
    generate_contract_pdf(contract, filepath)
    
    return send_file(filepath, as_attachment=True, attachment_filename=filename)
