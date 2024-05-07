from locust import HttpUser, task,FastHttpUser

class HelloWorldUser(FastHttpUser):
    @task
    def hello_world(self):
        self.client.client.clientpool.close()
        self.client.get("/driverprofile/",headers={'Authorization':'Token 1faac6261e834d406fe84d3b3561413fc579d2a5'})
