"""changed some field names in address model

Revision ID: 141fdf285401
Revises: 16a2461460c5
Create Date: 2023-02-12 18:37:05.007302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '141fdf285401'
down_revision = '16a2461460c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city_or_town', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('state_or_county', sa.String(length=256), nullable=False))
        batch_op.drop_column('state_or_province')
        batch_op.drop_column('city')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('state_or_province', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
        batch_op.drop_column('state_or_county')
        batch_op.drop_column('city_or_town')

    # ### end Alembic commands ###