import click
from api.models import db, Product

def setup_commands(app):
    @app.cli.command("seed")
    def seed():
        """(Tu seed actual, déjalo como esté o elimínalo si usarás reset_products)"""
        pass

    @app.cli.command("reset_products")
    def reset_products():
        """Borra todos los productos y carga el catálogo Suds (8 items) con rutas relativas."""
        db.session.query(Product).delete()

        items = [
            dict(name="Lavanda Calmante", description="Hecho a mano con aceites vegetales. Ideal para relajación nocturna.", price=6.90, image_url="/static/images/lavanda.jpg", aroma="Lavanda", ritual="Relajación nocturna"),
            dict(name="Exfoliante de Café y Coco", description="Exfoliación suave con café molido y aceite de coco.", price=8.50, image_url="/static/images/jabon_cafe_coco.jpg", aroma="Café y Coco", ritual="Energía matutina"),
            dict(name="Menta Refrescante", description="Frescura intensa y sensación revitalizante.", price=7.75, image_url="/static/images/menta.jpg", aroma="Menta", ritual="Ducha matutina"),
            dict(name="Rosas Hidratante", description="Suaviza e hidrata con delicado aroma floral.", price=9.99, image_url="/static/images/rosas.jpg", aroma="Rosas", ritual="Baño relajante"),
            dict(name="Limón y Jengibre Energizante", description="Cítrico picante para despertar cuerpo y mente.", price=7.99, image_url="/static/images/limon_jengibre.jpg", aroma="Limón y Jengibre", ritual="Impulso matinal"),
            dict(name="Avena y Miel Suavizante", description="Calma e hidrata pieles sensibles.", price=8.90, image_url="/static/images/avena_miel.jpg", aroma="Avena y Miel", ritual="Rutina diaria suave"),
            dict(name="Aloe Vera Reparador", description="Refresca y ayuda a reparar la piel.", price=8.50, image_url="/static/images/aloe_vera.jpg", aroma="Aloe Vera", ritual="After-sun o post-gym"),
            dict(name="Carbón Activado Purificante", description="Limpieza profunda para piel mixta/grasa.", price=9.50, image_url="/static/images/carbon_activado.jpg", aroma="Tierra fresca", ritual="Uso focal en zonas con grasa"),
        ]

        for data in items:
            db.session.add(Product(**data))

        db.session.commit()
        click.echo("Catálogo Suds ✅ (8 productos)")
