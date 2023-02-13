from locust import HttpUser, task


class FibonacciDjangoTest(HttpUser):
    @task
    def fibonacci(self):
        self.client.get("/fibonacci/")
