from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, UniqueConstraint

from app.db.base import Base


class MainMenu(Base):
    __tablename__ = 'main_menu'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('title', name='uq_main_menu_title'),
    )


class SubMenu(Base):
    __tablename__ = 'sub_menu'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    main_menu_id = Column(
        Integer, ForeignKey('main_menu.id', ondelete='CASCADE'), nullable=False
    )
    __table_args__ = (
        UniqueConstraint('title', name='uq_sub_menu_title'),
    )


class Dishes(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    sub_menu_id = Column(
        Integer, ForeignKey('sub_menu.id', ondelete='CASCADE'), nullable=False
    )
    price = Column(Numeric(precision=18, scale=2), nullable=True)

    __table_args__ = (
        UniqueConstraint('title', name='uq_dishes_title'),
    )
