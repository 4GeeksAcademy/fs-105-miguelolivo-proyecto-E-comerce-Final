from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

#USER

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

# PRODUCT

class Product(db.Model):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    aroma: Mapped[str] = mapped_column(String(80), nullable=True)
    ritual: Mapped[str] = mapped_column(Text, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url,
            "aroma": self.aroma,
            "ritual": self.ritual
        }

# CART 

class CartItem(db.Model):
    __tablename__ = "cart_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    product = relationship("Product", lazy="joined")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "product": self.product.serialize() if self.product else None,
        }

# ORDERS

class Order(db.Model):
    __tablename__ = "purchase_order"  # evitar palabra reservada "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")  # pending|paid|failed
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="joined")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "total": float(self.total),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "items": [i.serialize() for i in self.items],
        }

class OrderItem(db.Model):
    __tablename__ = "order_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("purchase_order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", lazy="joined")

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "product": self.product.serialize() if self.product else None,
        }
