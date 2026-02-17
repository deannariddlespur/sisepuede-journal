from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0008_aboutpage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutpage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='about/'),
        ),
    ]
