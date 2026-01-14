# ============================================================================
# app/routes/leads.py
# ============================================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Lead, Organization, Product

leads_bp = Blueprint('leads', __name__, url_prefix='/leads')

@leads_bp.route('/')
@login_required
def list_leads():
    leads = Lead.query.all()
    return render_template('leads/list.html', leads=leads)

@leads_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_lead():
    if request.method == 'POST':
        lead = Lead(
            organization_id=request.form['organization_id'],
            product_id=request.form['product_id'],
            owner_user_id=current_user.id,
            created_by_user_id=current_user.id,
            stage=request.form.get('stage', 'New'),
            temperature=request.form.get('temperature', 'Warm'),
            source=request.form.get('source'),
            first_contact_date=datetime.strptime(request.form['first_contact_date'], '%Y-%m-%d').date() if request.form.get('first_contact_date') else None,
            next_follow_up_date=datetime.strptime(request.form['next_follow_up_date'], '%Y-%m-%d').date() if request.form.get('next_follow_up_date') else None,
            notes=request.form.get('notes')
        )
        db.session.add(lead)
        db.session.commit()
        flash('Lead created successfully!', 'success')
        return redirect(url_for('leads.list_leads'))

    organizations = Organization.query.all()
    products = Product.query.filter_by(active=True).all()
    return render_template('leads/form.html', lead=None, organizations=organizations, products=products)

@leads_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_lead(id):
    lead = Lead.query.get_or_404(id)

    if request.method == 'POST':
        lead.organization_id = request.form['organization_id']
        lead.product_id = request.form['product_id']
        lead.stage = request.form.get('stage')
        lead.temperature = request.form.get('temperature')
        lead.source = request.form.get('source')
        lead.first_contact_date = datetime.strptime(request.form['first_contact_date'], '%Y-%m-%d').date() if request.form.get('first_contact_date') else None
        lead.next_follow_up_date = datetime.strptime(request.form['next_follow_up_date'], '%Y-%m-%d').date() if request.form.get('next_follow_up_date') else None
        lead.notes = request.form.get('notes')
        lead.status = request.form.get('status', 'Active')
        db.session.commit()
        flash('Lead updated successfully!', 'success')
        return redirect(url_for('leads.view_lead', id=id))

    organizations = Organization.query.all()
    products = Product.query.filter_by(active=True).all()
    return render_template('leads/form.html', lead=lead, organizations=organizations, products=products)

@leads_bp.route('/<int:id>')
@login_required
def view_lead(id):
    lead = Lead.query.get_or_404(id)
    return render_template('leads/view.html', lead=lead)
