import click
from api.models import db, Product

def setup_commands(app):

    @app.cli.command("insert-products")
    def insert_products():
        print("🧼 Limpiando productos existentes...")
        db.session.query(Product).delete()
        db.session.commit()

        print("🧼 Insertando productos de ejemplo...")

        products = [
            Product(
                name="Jabón Lavanda & Miel",
                description="Calma tu piel y sentidos con esta mezcla relajante.",
                price=8.99,
                image_url="https://es.pinterest.com/pin/42925002694495840/",
                aroma="Lavanda",
                ritual="Úsalo por la noche con agua tibia y movimientos circulares."
            ),
            Product(
                name="Jabón Cítrico Vital",
                description="Energía pura en cada ducha.",
                price=7.99,
                image_url="https://es.pinterest.com/pin/712342866097355036/",
                aroma="Naranja y Limón",
                ritual="Ideal para usar por la mañana, en duchas cortas y revitalizantes."
            ),
            Product(
                name="Jabón de Carbón Activado",
                description="Purifica y equilibra tu piel grasa o con impurezas.",
                price=9.50,
                image_url="https://es.pinterest.com/pin/586171707782115781/",
                aroma="Tierra fresca",
                ritual="Aplica suavemente en zonas propensas a grasa. Enjuaga bien."
            ),
            Product(
                name="Jabón de Rosas",
                description="Delicado aroma floral para piel suave.",
                price=9.99,
                image_url="https://es.pinterest.com/pin/2111131066479920/",
                aroma="Rosas",
                ritual="Úsalo para relajarte por la noche."
            ),
            Product(
                name="Jabón de Aloe Vera",
                description="Hidrata y calma la piel sensible.",
                price=8.50,
                image_url="https://es.pinterest.com/pin/3588874692586848/",
                aroma="Aloe Vera",
                ritual="Perfecto para pieles delicadas."
            ),
            Product(
                name="Jabón Exfoliante de Café",
                description="Elimina células muertas y revitaliza la piel.",
                price=10.00,
                image_url="https://es.pinterest.com/pin/8444318046893058/",
                aroma="Café tostado",
                ritual="Masajear suavemente antes de enjuagar."
            ),
            Product(
                name="Jabón de Menta Refrescante",
                description="Refresca y despierta los sentidos.",
                price=7.75,
                image_url="https://es.pinterest.com/pin/977562662876105753/",
                aroma="Menta",
                ritual="Ideal para duchas matutinas."
            ),
            Product(
                name="Jabón de Lavanda y Romero",
                description="Relajante y estimulante al mismo tiempo.",
                price=9.20,
                image_url="https://es.pinterest.com/pin/71424344085316782/",
                aroma="Lavanda y Romero",
                ritual="Úsalo para un baño relajante."
            ),
            Product(
                name="Jabón de Cacao y Vainilla",
                description="Nutre y suaviza la piel con aroma dulce.",
                price=9.80,
                image_url="https://es.pinterest.com/pin/52706258130748841/",
                aroma="Cacao y Vainilla",
                ritual="Perfecto para uso diario."
            ),
            Product(
                name="Jabón de Té Verde",
                description="Antioxidante y refrescante para la piel.",
                price=8.95,
                image_url="https://es.pinterest.com/pin/712342866097355036/",
                aroma="Té Verde",
                ritual="Usar en la mañana para revitalizar."
            ),
        ]

        db.session.add_all(products)
        db.session.commit()

        print("Productos añadidos correctamente.")
