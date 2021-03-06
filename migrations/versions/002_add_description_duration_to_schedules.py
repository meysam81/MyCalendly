"""add description & duration to schedules

Revision ID: adeed1048af4
Revises: 20b80d6bd5ea
Create Date: 2021-06-06 19:25:52.199835

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "adeed1048af4"
down_revision = "20b80d6bd5ea"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "schedules", sa.Column("description", sa.String(length=512), nullable=True)
    )
    op.add_column("schedules", sa.Column("duration", sa.Integer(), nullable=True))
    # ### end Alembic commands ###
    op.execute("UPDATE schedules SET duration = 0 WHERE duration IS NULL")
    op.alter_column("schedules", "duration", nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("schedules", "duration")
    op.drop_column("schedules", "description")
    # ### end Alembic commands ###
