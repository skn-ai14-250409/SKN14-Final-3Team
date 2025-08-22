# from django.core.management.base import BaseCommand
# from faker import Faker
# from user.models import User, Department, Position
# import random

# class Command(BaseCommand):
#     help = "Seed 100 users with dummy data"

#     def handle(self, *args, **kwargs):
#         fake = Faker("ko_KR")

#         dept = Department.objects.first()
#         pos = Position.objects.first()

#         for _ in range(100):
#             User.objects.create(
#                 employee_id=f"S{fake.random_int(min=230000, max=239999)}",
#                 email=fake.unique.email(),
#                 password="test1234",  # 실제론 hash 처리 필요
#                 name=fake.name(),
#                 position=pos,
#                 department=dept,
#                 hire_date=fake.date_between(start_date="-5y", end_date="today"),
#                 mobile=fake.phone_number(),
#                 birthdate=fake.date_of_birth(minimum_age=20, maximum_age=60),
#             )

#         self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 100 users"))
