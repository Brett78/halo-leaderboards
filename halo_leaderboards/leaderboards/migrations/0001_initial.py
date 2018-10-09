
# Generated by Django 2.0.9 on 2018-10-09 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('ref', models.IntegerField(db_index=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gamer_tag', models.CharField(db_index=True, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(max_length=255)),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csr', models.IntegerField(db_index=True)),
                ('rank', models.IntegerField(db_index=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='leaderboards.Player')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaderboards.Playlist')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(db_index=True, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(db_index=True)),
                ('end_date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(db_index=True)),
                ('image_url', models.CharField(max_length=255)),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaderboards.Designation')),
            ],
        ),
        migrations.AddField(
            model_name='rank',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaderboards.Season'),
        ),
        migrations.AddField(
            model_name='rank',
            name='tier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='leaderboards.Tier'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaderboards.Season'),
        ),
        migrations.AlterUniqueTogether(
            name='rank',
            unique_together={('player', 'playlist', 'season')},
        ),
    ]
