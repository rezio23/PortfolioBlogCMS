from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_siteconfiguration_education_telegram_group_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="threads_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="x_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="youtube_url",
            field=models.URLField(blank=True),
        ),
    ]
