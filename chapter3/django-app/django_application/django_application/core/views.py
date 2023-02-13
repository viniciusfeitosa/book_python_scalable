import random

from rest_framework import views
from rest_framework.response import Response

from .models import fibonacci
from .serializers import FibSerializer


class FibView(views.APIView):

    def get(self, request):
        random_num = random.randint(1, 10)
        results = FibSerializer({
            'random_num': random_num,
            'fib_result': fibonacci(random_num),
        }).data
        return Response(results)
