# Generated by Django 3.1.2 on 2021-05-02 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gacha', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gachaitem',
            name='rare',
            field=models.CharField(choices=[('VR', 'バンタン限定'), ('SR', 'スーパーレア'), ('R', 'レア'), ('N', 'ノーマル')], default='N', max_length=10, verbose_name='レア度'),
        ),
    ]
