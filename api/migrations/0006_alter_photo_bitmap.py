from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_location_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='bitmap',
            field=models.BinaryField(default=b''),
        ),
    ]
