from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("operadoras", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="operadora",
            options={"managed": False},
        ),
    ]
