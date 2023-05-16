"""init

Revision ID: 41c35fcd8655
Revises: 
Create Date: 2023-05-15 11:30:40.769065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "41c35fcd8655"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column(
            "phone",
            sa.Integer,
            nullable=False,
            autoincrement=False,
            info={"min_digits": 10, "max_digits": 10},
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
