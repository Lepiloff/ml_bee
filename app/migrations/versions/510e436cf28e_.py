"""empty message

Revision ID: 510e436cf28e
Revises: 
Create Date: 2019-03-25 08:28:51.156850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '510e436cf28e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img_filename', sa.String(), nullable=True),
    sa.Column('counter', sa.Integer(), nullable=True),
    sa.Column('img_data', sa.String(length=264), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
