"""deployment

Revision ID: 6fc5b4eee45f
Revises: 
Create Date: 2024-08-04 20:53:05.924457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fc5b4eee45f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('assets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('allocated_to', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['allocated_to'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.String(length=200), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('urgency', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requests')
    op.drop_table('assets')
    op.drop_table('users')
    # ### end Alembic commands ###
