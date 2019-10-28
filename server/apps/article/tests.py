from django.test import TestCase

# Create your tests here.
import random
from user.models import User

test_user = User.objects.filter(true_name='测试用户')
sum = test_user.count()
done = 0
for user in test_user:
	user.school_account = f'{random.random()}{user.id}'[-9:]
	user.save()
	print(user.school_account)
	print(f'{done}/{sum}')

