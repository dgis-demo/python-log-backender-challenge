from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOutbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=255)),
                ('event_date_time', models.DateTimeField()),
                ('event_context', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
