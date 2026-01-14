# ============================================================================
# app/routes/main.py
# ============================================================================

from flask import Blueprint, render_template
from flask_login import login_required
from app import db
from app.models import Product, Organization, Lead, Interaction
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    # Basic stats
    stats = {
        'products': Product.query.filter_by(active=True).count(),
        'organizations': Organization.query.count(),
        'leads': Lead.query.filter_by(status='Active').count(),
        'interactions': Interaction.query.count()
    }

    # Lead stage distribution
    stage_stats = db.session.query(
        Lead.stage,
        func.count(Lead.id)
    ).filter_by(status='Active').group_by(Lead.stage).all()

    # Temperature distribution
    temp_stats = db.session.query(
        Lead.temperature,
        func.count(Lead.id)
    ).filter_by(status='Active').group_by(Lead.temperature).all()

    # Conversion stats
    total_leads = Lead.query.count()
    closed_won = Lead.query.filter_by(stage='Closed Won').count()
    conversion_rate = round((closed_won / total_leads * 100) if total_leads > 0 else 0, 1)

    recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(5).all()

    analytics = {
        'stage_distribution': dict(stage_stats),
        'temperature_distribution': dict(temp_stats),
        'conversion_rate': conversion_rate,
        'total_leads': total_leads,
        'closed_won': closed_won
    }

    return render_template('dashboard.html', stats=stats, recent_leads=recent_leads, analytics=analytics)
