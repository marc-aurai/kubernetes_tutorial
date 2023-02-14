from locust import HttpUser, task, between
import json

class AppUser(HttpUser):
    wait_time = between(0.1,1.5)
    
    @task
    def predict_page(self):
        data_fastapi = {"question1": ["Is this a question from someone that works in Amsterdam?"],
                        "question2": ["Is this a question from a person that works in Amsterdam?"]}

        headers = {'Content-Type': 'application/json'}

        resp = self.client.post("/predict/", data=json.dumps(data_fastapi), headers=headers)
        print(resp.content)