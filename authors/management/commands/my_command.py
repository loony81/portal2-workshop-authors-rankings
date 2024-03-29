import django
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.db import DEFAULT_DB_ALIAS

"""
python manage.py createsuperuser --username admin --password admin
python manage.py createsuperuser --username admin --password admin --email foo@foo.foo
"""

class Command(createsuperuser.Command):
    help = 'create/update a superuser with password'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--password', dest='password', default=None)

    def handle(self, *args, **options):
        username = options.get('username')
        password = options.get('password')
        email = options.get('email')

        database = DEFAULT_DB_ALIAS
        if not password or not username:
            raise CommandError("--username and --password are required")

        data = {'username': username,'password': password,'email': email}
        # User.objects.create_superuser(username='name',email='email',password='password')
        try:
            self.UserModel._default_manager.db_manager(database).create_superuser(**data)
        except django.db.utils.IntegrityError:
            user = self.UserModel._default_manager.db_manager(database).get(username=username)
            user.set_password(password)
            if email:
                user.email = email
            user.save()