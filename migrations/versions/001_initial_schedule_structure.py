"""initial schedule structure

Revision ID: 20b80d6bd5ea
Revises:
Create Date: 2021-06-05 11:58:02.951499

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20b80d6bd5ea"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("timeframes", sa.String(length=2 ** 15), nullable=False),
        sa.Column("created_ts", sa.DateTime(), nullable=False),
        sa.Column("updated_ts", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_schedules_name"), "schedules", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_schedules_name"), table_name="schedules")
    op.drop_table("schedules")
    # ### end Alembic commands ###
