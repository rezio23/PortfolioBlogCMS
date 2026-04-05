from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_siteconfiguration_site_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="contact_email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="facebook_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="github_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="instagram_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="tiktok_url",
            field=models.URLField(blank=True),
        ),
    ]
