"""Seed script to populate the database with initial data."""
from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.product import Product, ProductCategory
from app.core.enums import UserRole, AvailabilityStatus

def seed():
    from app.core.database import init_db
    eng, sess = init_db()
    Base.metadata.create_all(bind=eng)
    db = sess()
    try:
        if db.query(User).count() == 0:
            admin = User(
                name="Admin",
                email="admin@interservim.com",
                password_hash=hash_password("Admin123!"),
                role=UserRole.ADMIN,
            )
            db.add(admin)
            manager = User(
                name="Manager",
                email="manager@interservim.com",
                password_hash=hash_password("Manager123!"),
                role=UserRole.MANAGER,
            )
            db.add(manager)
            reidelio = User(
                name="Reidelio",
                email="reidelio@interservim.com",
                password_hash=hash_password("TuTy123"),
                role=UserRole.ADMIN,
            )
            db.add(reidelio)
            db.flush()
        if db.query(ProductCategory).count() == 0:
            grains = ProductCategory(name="Granos", description="Cereales, legumbres y granos básicos")
            db.add(grains)
            db.flush()
            products = [
                Product(name="Arroz Blanco Premium", sku="ARZ-001", category_id=grains.id, description="Arroz blanco de grano largo, cosecha 2024. Ideal para consumo humano.", brand="Premium Grain", origin_country="Vietnam", unit_price=450.00, currency="USD", minimum_order_quantity=1000, packaging="Sacos de 50kg", availability_status=AvailabilityStatus.AVAILABLE, container_capacity="20 MT por contenedor 20'"),
                Product(name="Arroz Blanco Estándar", sku="ARZ-002", category_id=grains.id, description="Arroz blanco de grano medio, calidad estándar.", brand="Standard Grain", origin_country="Tailandia", unit_price=380.00, currency="USD", minimum_order_quantity=2000, packaging="Sacos de 50kg", availability_status=AvailabilityStatus.AVAILABLE, container_capacity="22 MT por contenedor 20'"),
                Product(name="Azúcar Refinada", sku="AZU-001", category_id=grains.id, description="Azúcar refinada de caña, blanca, grado ICUMSA 45.", brand="SweetCane", origin_country="Brasil", unit_price=380.00, currency="USD", minimum_order_quantity=5000, packaging="Sacos de 50kg", availability_status=AvailabilityStatus.AVAILABLE, container_capacity="26 MT por contenedor 20'"),
                Product(name="Maíz Amarillo", sku="MAZ-001", category_id=grains.id, description="Maíz amarillo duro, grado #2, no transgénico.", brand="GoldenCorn", origin_country="Estados Unidos", unit_price=320.00, currency="USD", minimum_order_quantity=5000, packaging="A granel", availability_status=AvailabilityStatus.AVAILABLE, container_capacity="28 MT por contenedor 20'"),
                Product(name="Frijol Negro", sku="FRJ-001", category_id=grains.id, description="Frijol negro de alta calidad, cosecha 2024.", brand="BlackBean", origin_country="Uganda", unit_price=550.00, currency="USD", minimum_order_quantity=1000, packaging="Sacos de 50kg", availability_status=AvailabilityStatus.AVAILABLE, container_capacity="20 MT por contenedor 20'"),
            ]
            for p in products:
                db.add(p)
            db.commit()
            print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
