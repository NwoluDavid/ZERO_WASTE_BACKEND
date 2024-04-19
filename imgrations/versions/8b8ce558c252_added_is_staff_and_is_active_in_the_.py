"""added is_staff and is_active in the user table

Revision ID: 8b8ce558c252
Revises: 
Create Date: 2024-04-19 11:21:58.862175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '8b8ce558c252'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('display_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('review',
    sa.Column('reviewer_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_id'), 'review', ['id'], unique=False)
    op.create_table('waste',
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('phone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pickup_date', sa.Date(), nullable=False),
    sa.Column('waste_type', sa.Enum('organic_waste', 'plastic_waste', 'medical_waste', name='wastetype'), nullable=False),
    sa.Column('user_waste', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('amount', sa.Enum('organic_waste', 'plastic_waste', 'medical_waste', 'industrial_waste', name='amount'), nullable=False),
    sa.Column('order_status', sa.Enum('pending', 'in_transit', 'delivered', name='bookingstatus'), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('waste')
    op.drop_index(op.f('ix_review_id'), table_name='review')
    op.drop_table('review')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
