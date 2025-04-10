"""initial migration

Revision ID: initial
Revises: 
Create Date: 2024-03-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sui_address', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('bio', sa.String(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sui_address'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # Create properties table
    op.create_table(
        'properties',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False, server_default='SUI'),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('bedrooms', sa.Integer(), nullable=False),
        sa.Column('bathrooms', sa.Integer(), nullable=False),
        sa.Column('area', sa.Float(), nullable=False),
        sa.Column('property_type', sa.String(), nullable=False),
        sa.Column('token_id', sa.String(), nullable=True),
        sa.Column('owner_address', sa.String(), nullable=False),
        sa.Column('is_listed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('images', postgresql.JSONB(), nullable=False, server_default='[]'),
        sa.Column('documents', postgresql.JSONB(), nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_id')
    )
    
    # Create user_favorites table
    op.create_table(
        'user_favorites',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'property_id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_properties_location'), 'properties', ['location'], unique=False)
    op.create_index(op.f('ix_properties_owner_address'), 'properties', ['owner_address'], unique=False)
    op.create_index(op.f('ix_properties_property_type'), 'properties', ['property_type'], unique=False)
    op.create_index(op.f('ix_properties_title'), 'properties', ['title'], unique=False)
    op.create_index(op.f('ix_users_sui_address'), 'users', ['sui_address'], unique=True)

def downgrade():
    op.drop_index(op.f('ix_users_sui_address'), table_name='users')
    op.drop_index(op.f('ix_properties_title'), table_name='properties')
    op.drop_index(op.f('ix_properties_property_type'), table_name='properties')
    op.drop_index(op.f('ix_properties_owner_address'), table_name='properties')
    op.drop_index(op.f('ix_properties_location'), table_name='properties')
    op.drop_table('user_favorites')
    op.drop_table('properties')
    op.drop_table('users') 