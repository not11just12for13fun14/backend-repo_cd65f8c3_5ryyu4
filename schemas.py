"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Cleaning business specific schemas

class Lead(BaseModel):
    """
    Leads/Quote requests from website visitors
    Collection name: "lead"
    """
    name: str = Field(..., description="Full name of the requester")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone number")
    service_type: Literal[
        "Nettoyage résidentiel",
        "Nettoyage commercial",
        "Fin de bail",
        "Nettoyage de vitres",
        "Entretien récurrent",
        "Autre"
    ] = Field("Autre", description="Type de service demandé")
    address: Optional[str] = Field(None, description="Adresse à Lausanne / région")
    message: Optional[str] = Field(None, description="Détails supplémentaires")
    preferred_date: Optional[str] = Field(None, description="Date souhaitée")

class ContactMessage(BaseModel):
    """
    Simple contact messages
    Collection name: "contactmessage"
    """
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
