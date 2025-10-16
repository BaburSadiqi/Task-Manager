"""add task enums"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '6cd03cc4eaca'
down_revision = '3d89d855f0c0'
branch_labls = None
depends_on = None


def upgrade() -> None:
    # Create PostgreSQL enums for status and priority 
    place_status_enum = postgresql.ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='placestatus')
    place_status_enum.create(op.get_bind())

    priority_enum = postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', name='priority')
    priority_enum.create(op.get_bind())


def downgrade() -> None:
    # drop enmus in revers order
    priority_enum = postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', name='priority')
    priority_enum.drop(op.get_bind)

    place_status_enum = postgresql.ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='placestatus')
    place_status_enum.drop(op.get_bind) 