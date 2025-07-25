"""update table friends

Revision ID: 89f64eaf657d
Revises: 63d5d4079137
Create Date: 2025-04-19 19:38:36.251404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89f64eaf657d'
down_revision: Union[str, None] = '63d5d4079137'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friends', sa.Column('friend_name', sa.String(), nullable=False))
    op.create_foreign_key(None, 'friends', 'users', ['friend_name'], ['username'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'friends', type_='foreignkey')
    op.drop_column('friends', 'friend_name')
    # ### end Alembic commands ###
