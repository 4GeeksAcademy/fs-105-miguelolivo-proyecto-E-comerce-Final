import click
from api.models import db, User, Product  

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are useful to run cronjobs or tasks outside of the API but still in integration 
with your database, for example: Import the price of bitcoin every night at 12am.
"""

def setup_commands(app):
    
    @app.cli.command("insert-test-users")  # name of our command
    @click.argument("count")  # argument of our command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")
        print("All test users created")

    @app.cli.command("insert-products")
    def insert_products():
        print("🧼 Insertando productos de ejemplo...")

        product1 = Product(
            name="Jabón Lavanda & Miel",
            description="Calma tu piel y sentidos con esta mezcla relajante.",
            price=8.99,
            image_url="",
            aroma="Lavanda",
            ritual="Úsalo por la noche con agua tibia y movimientos circulares."
        )

        product2 = Product(
            name="Jabón Cítrico Vital",
            description="Energía pura en cada ducha.",
            price=7.99,
            image_url="",
            aroma="Naranja y Limón",
            ritual="Ideal para usar por la mañana, en duchas cortas y revitalizantes."
        )

        product3 = Product(
            name="Jabón de Carbón Activado",
            description="Purifica y equilibra tu piel grasa o con impurezas.",
            price=9.50,
            image_url="",
            aroma="Tierra fresca",
            ritual="Aplica suavemente en zonas propensas a grasa. Enjuaga bien."
        )

        db.session.add_all([product1, product2, product3])
        db.session.commit()

        print("Productos añadidos correctamente.")

