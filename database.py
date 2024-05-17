from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Corrected DATABASE_URL format for MySQL
DATABASE_URL = "mysql+asyncmy://root:prajwal2708@localhost/findturf"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker for async sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
