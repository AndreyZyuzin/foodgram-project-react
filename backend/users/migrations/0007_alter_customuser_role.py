# Generated by Django 4.2.2 on 2023-06-29 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('guest', 'Guest'), ('user', 'User'), ('admin', 'Admin')], default='user', max_length=20, verbose_name='Роль пользователя'),
        ),
    ]