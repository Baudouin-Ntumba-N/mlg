from django.test import TestCase, Client

c =  Client()

response = c.post("/login/", {"username":"BDN",  "password":"bdn18mars"})

assert response.status_code == 200

# Create your tests here.
