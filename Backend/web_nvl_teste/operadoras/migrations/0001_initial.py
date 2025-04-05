from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Operadora",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("registro_ans", models.CharField(max_length=20)),
                ("cnpj", models.CharField(max_length=20)),
                ("razao_social", models.CharField(max_length=255)),
                ("nome_fantasia", models.CharField(max_length=255)),
            ],
        ),
    ]
