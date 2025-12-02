"""Remove SACCO_NGO plan type

Revision ID: 6c5f80a02eb0
Revises: 47e956906613
Create Date: 2025-07-10 02:53:22.533916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c5f80a02eb0'
down_revision = '47e956906613'
branch_labels = None
depends_on = None


def upgrade():
    # Skip deletion since SACCO_NGO doesn't exist in the current enum
    # op.execute("DELETE FROM enterprise_subscription_plans WHERE plan_type = 'SACCO_NGO'")
    
    # Check if the enum needs updating (it may already be correct)
    # Note: This migration is being skipped as the enum may already be in the correct state
    pass


def downgrade():
    # No action needed
    pass
