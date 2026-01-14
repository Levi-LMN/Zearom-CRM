# ============================================================================
# app/models.py
# ============================================================================

from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150))
    profile_picture = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships - specify foreign_keys to avoid ambiguity
    leads_owned = db.relationship('Lead', foreign_keys='Lead.owner_user_id', backref='owner', lazy=True)
    leads_created = db.relationship('Lead', foreign_keys='Lead.created_by_user_id', backref='created_by', lazy=True)
    products_created = db.relationship('Product', backref='created_by', lazy=True)
    organizations_created = db.relationship('Organization', backref='created_by', lazy=True)
    contacts_created = db.relationship('Contact', backref='created_by', lazy=True)
    interactions_created = db.relationship('Interaction', backref='created_by', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    leads = db.relationship('Lead', backref='product', lazy=True)

class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(200))
    size = db.Column(db.String(50))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    contacts = db.relationship('Contact', backref='organization', lazy=True, cascade='all, delete-orphan')
    leads = db.relationship('Lead', backref='organization', lazy=True)

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(150))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lead(db.Model):
    __tablename__ = 'leads'

    STAGES = ['New', 'Reached', 'Interested', 'Demo Scheduled', 'Pilot', 'Pricing', 'Closed Won', 'Closed Lost']
    TEMPERATURES = ['Hot', 'Warm', 'Cold']
    SOURCES = ['Referral', 'Outbound', 'Inbound', 'Partner', 'Event', 'Other']
    STATUSES = ['Active', 'Closed']

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    stage = db.Column(db.String(50), nullable=False, default='New')
    temperature = db.Column(db.String(20), default='Warm')
    source = db.Column(db.String(50))
    first_contact_date = db.Column(db.Date)
    next_follow_up_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    interactions = db.relationship('Interaction', backref='lead', lazy=True, cascade='all, delete-orphan')

class Interaction(db.Model):
    __tablename__ = 'interactions'

    TYPES = ['Call', 'Email', 'Demo', 'Meeting', 'Follow-up', 'Other']

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    summary = db.Column(db.Text)
    outcome = db.Column(db.Text)
    next_action = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
