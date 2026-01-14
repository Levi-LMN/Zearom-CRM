# ============================================================================
# app/routes/interactions.py
# ============================================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Interaction, Lead

interactions_bp = Blueprint('interactions', __name__, url_prefix='/interactions')

@interactions_bp.route('/lead/<int:lead_id>/add', methods=['POST'])
@login_required
def add_interaction(lead_id):
    interaction = Interaction(
        lead_id=lead_id,
        created_by_user_id=current_user.id,
        interaction_type=request.form['interaction_type'],
        date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
        summary=request.form.get('summary'),
        outcome=request.form.get('outcome'),
        next_action=request.form.get('next_action')
    )
    db.session.add(interaction)
    db.session.commit()
    flash('Interaction logged successfully!', 'success')
    return redirect(url_for('leads.view_lead', id=lead_id))

@interactions_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_interaction(id):
    interaction = Interaction.query.get_or_404(id)

    if request.method == 'POST':
        interaction.interaction_type = request.form['interaction_type']
        interaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        interaction.summary = request.form.get('summary')
        interaction.outcome = request.form.get('outcome')
        interaction.next_action = request.form.get('next_action')
        db.session.commit()
        flash('Interaction updated successfully!', 'success')
        return redirect(url_for('leads.view_lead', id=interaction.lead_id))

    return render_template('interactions/form.html', interaction=interaction)

@interactions_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_interaction(id):
    interaction = Interaction.query.get_or_404(id)
    lead_id = interaction.lead_id
    db.session.delete(interaction)
    db.session.commit()
    flash('Interaction deleted successfully!', 'success')
    return redirect(url_for('leads.view_lead', id=lead_id))
