"""crete users

Revision ID: 5946daf479bb
Revises: 
Create Date: 2024-01-11 11:58:02.272943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '5946daf479bb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('first_name', sa.Text),
        sa.Column('last_name', sa.Text),
        sa.Column('email', sa.Text),
        sa.Column('created_at', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False),
    )

    op.create_table(
        'candidates',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('first_name', sa.Text),
        sa.Column('last_name', sa.Text),
        sa.Column('email', sa.Text),
        sa.Column('career_level', sa.Text),
        sa.Column('job_major', sa.Text),
        sa.Column('years_of_experience', sa.SmallInteger),
        sa.Column('skills', sa.ARRAY(sa.Text)),
        sa.Column('nationality', sa.Text),
        sa.Column('city', sa.Text),
        sa.Column('salary', sa.Float),
        sa.Column('gender', sa.Text),
        sa.Column('created_at', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('candidates')
