"""init

Revision ID: de9cefab5c6d
Revises: 603ab1ca431a
Create Date: 2025-02-02 23:45:31.555541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de9cefab5c6d'
down_revision: Union[str, None] = '603ab1ca431a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instagram_messages', sa.Column('sender_id', sa.BigInteger(), nullable=False))
    op.add_column('instagram_messages', sa.Column('recipient_id', sa.BigInteger(), nullable=False))
    op.drop_constraint('instagram_messages_user_id_fkey', 'instagram_messages', type_='foreignkey')
    op.create_foreign_key(None, 'instagram_messages', 'instagram_user_profiles', ['sender_id'], ['id'])
    op.create_foreign_key(None, 'instagram_messages', 'instagram_user_profiles', ['recipient_id'], ['id'])
    op.drop_column('instagram_messages', 'user_id')
    op.create_unique_constraint(None, 'instagram_user_profiles', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'instagram_user_profiles', type_='unique')
    op.add_column('instagram_messages', sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'instagram_messages', type_='foreignkey')
    op.drop_constraint(None, 'instagram_messages', type_='foreignkey')
    op.create_foreign_key('instagram_messages_user_id_fkey', 'instagram_messages', 'instagram_user_profiles', ['user_id'], ['id'])
    op.drop_column('instagram_messages', 'recipient_id')
    op.drop_column('instagram_messages', 'sender_id')
    # ### end Alembic commands ###
