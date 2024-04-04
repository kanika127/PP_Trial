# Generated by Django 5.0.3 on 2024-04-04 11:37

import app1.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailVerificationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user_data', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='MyClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(default='', max_length=50)),
                ('industry', models.CharField(default='', max_length=50)),
                ('address', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('application_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected'), ('O', 'Other')], default='P', max_length=10)),
                ('other_status', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(unique=True)),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSampleWorkTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('link', models.URLField(max_length=128, verbose_name='sample_wrk_link')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=80)),
                ('serves_hot_dogs', models.BooleanField(default=False)),
                ('serves_pizza', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSampleWorkTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='uploads/', validators=[app1.models.UserSampleWorkTable.validate_file_extension])),
            ],
        ),
        migrations.CreateModel(
            name='PassionUser',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True)),
                ('sample_work', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_sample_work', to='app1.usersampleworktable')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('app1.baseuser',),
        ),
        migrations.CreateModel(
            name='SuperUser',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('admin_level', models.CharField(default='standard', max_length=100)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('app1.baseuser',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100)),
                ('medium', models.CharField(default=None, max_length=100)),
                ('approx_completion_date', models.DateField(default=None)),
                ('description', models.CharField(default=None, max_length=2000)),
                ('role_count', models.IntegerField(default=1)),
                ('project_status', models.CharField(choices=[('P', 'Pending'), ('L', 'Live'), ('MS', 'MatchSuccess'), ('NM', 'NoMatches'), ('C', 'Complete')], default=None, max_length=3)),
                ('sample_wrk', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='project_sample_work', to='app1.projectsampleworktable')),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pitched_projects', to='app1.passionuser')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.CharField(choices=[('PR', 'Photographer'), ('VR', 'Videographer'), ('FM', 'Filmmaker'), ('VE', 'Video Editor'), ('D', 'Dancer'), ('A', 'Artist'), ('MB', 'Musician / Band'), ('MP', 'Music Producer'), ('DJ', 'DJ'), ('INS', 'Instrumentalist'), ('WR', 'Writer'), ('PC', 'Podcaster'), ('SCW', 'Screenwriter'), ('FD', 'Fashion Designer'), ('M', 'Model'), ('STF', 'Startup Founder'), ('TB', 'Tech Builder'), ('WDES', 'Web Designer'), ('WDEV', 'Web Developer'), ('GMDES', 'Game Designer'), ('GRDES', 'Graphic Designer'), ('ANIM', 'Animator / VFX'), ('CRDEV', 'Creative Director'), ('INF', 'Influencer'), ('O', 'Other')], default='PR', max_length=5)),
                ('other_role_type', models.CharField(blank=True, max_length=100, null=True)),
                ('role_count', models.IntegerField()),
                ('collab_type', models.CharField(choices=[('P', 'Paid'), ('U', 'Unpaid'), ('C', 'Collaboration')], default='P', max_length=15)),
                ('budget', models.FloatField()),
                ('exec_mode', models.CharField(choices=[('P', 'in-person'), ('V', 'virtual')], default='P', max_length=15)),
                ('project', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='app1.project')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('passionuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app1.passionuser')),
                ('org_name', models.CharField(default='', max_length=100)),
                ('industry', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, size=None)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('app1.passionuser',),
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('passionuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app1.passionuser')),
                ('field', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, size=None)),
                ('pronoun', models.CharField(choices=[('H', 'He'), ('S', 'She'), ('O', 'Other')], default='O', max_length=10)),
                ('star_rating', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('app1.passionuser',),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('application_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=10)),
                ('ques', models.CharField(blank=True, max_length=1000)),
                ('role', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='app1.role')),
                ('applicant', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='app1.creator')),
            ],
        ),
    ]
