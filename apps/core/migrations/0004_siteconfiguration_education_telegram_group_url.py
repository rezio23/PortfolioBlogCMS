from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_siteconfiguration_contact_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="education_telegram_group_url",
            field=models.URLField(blank=True),
        ),
    ]
