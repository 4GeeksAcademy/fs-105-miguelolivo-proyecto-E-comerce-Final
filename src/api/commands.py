import click
from api.models import db, Product

def setup_commands(app):
    @app.cli.command("seed")
    def seed():
        """Carga datos de ejemplo de productos (sin slug)."""
        samples = [
            dict(
                name="Jabón de Lavanda Calmante",
                description="Hecho a mano con aceites vegetales. Ideal para relajación nocturna.",
                price=6.90,
                image_url="",
                aroma="lavanda",
                ritual="Relajación nocturna",
            ),
            dict(
                name="Exfoliante de Café y Coco",
                description="Exfoliación suave con aroma tropical.",
                price=8.50,
                image_url="",
                aroma="coco",
                ritual="Energía matutina",
            )
        ]

        created = 0
        for data in samples:
            exists = Product.query.filter_by(name=data["name"]).first()
            if not exists:
                db.session.add(Product(**data))
                created += 1
        db.session.commit()
        click.echo(f"Seeds cargados ✅ ({created} nuevos)")
