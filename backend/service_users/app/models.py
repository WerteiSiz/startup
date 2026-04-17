from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    PARTNER = "partner"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)  # soft delete: False = удалён
    deleted_at = Column(DateTime, nullable=True)  # когда запросил удаление
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    partner_request = relationship("PartnerRequest", back_populates="user", uselist=False)
    partner = relationship("Partner", back_populates="user", uselist=False)
    favorites = relationship("Favorite", back_populates="user")
    email_verifications = relationship("EmailVerification", back_populates="user")


class EmailVerification(Base):
    __tablename__ = "email_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="email_verifications")


class PartnerRequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PartnerRequest(Base):
    __tablename__ = "partner_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    company_name = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(PartnerRequestStatus), default=PartnerRequestStatus.PENDING)
    admin_comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="partner_request")


class Partner(Base):
    __tablename__ = "partners"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    company_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    is_approved = Column(Boolean, default=True)
    ads_limit = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="partner")
    ads = relationship("Ad", back_populates="partner")


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    is_custom = Column(Boolean, default=False)
    
    ads = relationship("Ad", secondary="ad_categories", back_populates="categories")


class Ad(Base):
    __tablename__ = "ads"
    
    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    discount_percent = Column(Integer, nullable=False)  # от 1 до 100
    url = Column(String, nullable=False)
    address = Column(String, nullable=False)
    end_date = Column(DateTime, nullable=False)
    clicks_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    emodzi_id = Column(Integer, nullable=True)  # ID эмоции/иконки
    prioritet = Column(Integer, default=0)  # приоритет отображения
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    partner = relationship("Partner", back_populates="ads")
    categories = relationship("Category", secondary="ad_categories", back_populates="ads")
    favorites = relationship("Favorite", back_populates="ad")


class AdCategory(Base):
    __tablename__ = "ad_categories"
    
    ad_id = Column(Integer, ForeignKey("ads.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)


class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ad_id = Column(Integer, ForeignKey("ads.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="favorites")
    ad = relationship("Ad", back_populates="favorites")