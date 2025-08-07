import os
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base  # Asegúrate de importar correctamente

config = context.config

# Obtener la URL desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://usuario:contraseña@host:puerto/basedatos")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
