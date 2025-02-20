from sqlmodel import Session, create_engine, select

from spaces.core.config import settings

engine = create_engine(str(settings.SQLALCEHMY_DATABASE_URI))

# Intilize Database 
