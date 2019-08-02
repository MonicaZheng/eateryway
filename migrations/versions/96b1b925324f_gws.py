"""gws

Revision ID: 96b1b925324f
Revises: 
Create Date: 2019-06-27 20:48:37.982634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96b1b925324f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('food',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_category'), 'food', ['category'], unique=False)
    op.create_index(op.f('ix_food_name'), 'food', ['name'], unique=True)
    op.create_table('pay_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('apt_num', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_address_address'), 'address', ['address'], unique=True)
    op.create_index(op.f('ix_address_apt_num'), 'address', ['apt_num'], unique=True)
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_order_date'), 'order', ['order_date'], unique=False)
    op.create_table('order_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_item_quantity'), 'order_item', ['quantity'], unique=False)
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('pay_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['pay_type_id'], ['pay_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payment_balance'), 'payment', ['balance'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payment_balance'), table_name='payment')
    op.drop_table('payment')
    op.drop_index(op.f('ix_order_item_quantity'), table_name='order_item')
    op.drop_table('order_item')
    op.drop_index(op.f('ix_order_order_date'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_address_apt_num'), table_name='address')
    op.drop_index(op.f('ix_address_address'), table_name='address')
    op.drop_table('address')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('pay_type')
    op.drop_index(op.f('ix_food_name'), table_name='food')
    op.drop_index(op.f('ix_food_category'), table_name='food')
    op.drop_table('food')
    # ### end Alembic commands ###
