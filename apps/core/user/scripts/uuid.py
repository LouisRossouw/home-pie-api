from user.models import User
from django.db.models import Count


def run():
    # duplicates = User.objects.values('UUID').annotate(
    #     uuid_count=Count('UUID')).filter(uuid_count__gt=1)
    # if duplicates.exists():
    #     print(f'Duplicates found: {duplicates}')
    # else:
    #     print('No duplicates found.')

    users_objects = User.objects.all()
    for i in users_objects:
        print(i)
