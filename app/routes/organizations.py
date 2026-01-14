# ============================================================================
# app/routes/organizations.py
# ============================================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Organization, Contact

organizations_bp = Blueprint('organizations', __name__, url_prefix='/organizations')

@organizations_bp.route('/')
@login_required
def list_organizations():
    organizations = Organization.query.all()
    return render_template('organizations/list.html', organizations=organizations)

@organizations_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_organization():
    if request.method == 'POST':
        org = Organization(
            name=request.form['name'],
            industry=request.form.get('industry'),
            location=request.form.get('location'),
            size=request.form.get('size'),
            created_by_user_id=current_user.id
        )
        db.session.add(org)
        db.session.commit()
        flash('Organization created successfully!', 'success')
        return redirect(url_for('organizations.list_organizations'))

    return render_template('organizations/form.html', organization=None)

@organizations_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_organization(id):
    org = Organization.query.get_or_404(id)

    if request.method == 'POST':
        org.name = request.form['name']
        org.industry = request.form.get('industry')
        org.location = request.form.get('location')
        org.size = request.form.get('size')
        db.session.commit()
        flash('Organization updated successfully!', 'success')
        return redirect(url_for('organizations.list_organizations'))

    return render_template('organizations/form.html', organization=org)

@organizations_bp.route('/<int:id>')
@login_required
def view_organization(id):
    org = Organization.query.get_or_404(id)
    return render_template('organizations/view.html', organization=org)

@organizations_bp.route('/<int:org_id>/contacts/add', methods=['POST'])
@login_required
def add_contact(org_id):
    contact = Contact(
        organization_id=org_id,
        name=request.form['name'],
        role=request.form.get('role'),
        phone=request.form.get('phone'),
        email=request.form.get('email'),
        created_by_user_id=current_user.id
    )
    db.session.add(contact)
    db.session.commit()
    flash('Contact added successfully!', 'success')
    return redirect(url_for('organizations.view_organization', id=org_id))

@organizations_bp.route('/contacts/<int:id>/delete', methods=['POST'])
@login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    org_id = contact.organization_id
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('organizations.view_organization', id=org_id))
