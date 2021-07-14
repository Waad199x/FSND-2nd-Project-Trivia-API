"""empty message

Revision ID: 3afae3a067de
Revises: d41db783a5c9
Create Date: 2021-06-23 08:09:44.611794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3afae3a067de'
down_revision = 'd41db783a5c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('showT',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Artist_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['Artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('show')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Artist_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('start_date', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['Artist_id'], ['Artist.id'], name='show_Artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='show_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='show_pkey')
    )
    op.drop_table('showT')
    # ### end Alembic commands ###
