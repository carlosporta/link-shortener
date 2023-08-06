from random import randint
from locust import FastHttpUser, task


class HelloWorldUser(FastHttpUser):
    count = 0

    @task
    def add_url(self):
        url = "127.0.0.1:8000/health"
        alias = str(self.count)
        json = {"url": url, "alias": alias}
        with self.client.post("/shorten", json=json, catch_response=True,) as response:
            if response.status_code == 409:
                response.success()
        self.count += 1

    @task(10)
    def redirect_url(self):
        if self.count == 0:
            return

        alias = str(randint(0, self.count - 1))
        url = f"/r/{alias}"
        self.client.get(url, name="/", allow_redirects=False) 
