"""all tables

Revision ID: 15ba1a30a261
Revises: 
Create Date: 2020-03-03 10:33:51.250111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15ba1a30a261'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('region', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('capability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('need',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('need')
    op.drop_table('capability')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('city')
    # ### end Alembic commands ###