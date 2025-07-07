from django.db import models

from utils.base_model import BaseModel


class User(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=60)
    company = models.CharField(max_length=4)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    theme = models.CharField(max_length=5)
    color = models.CharField(max_length=20)
    picture = models.URLField(max_length=200, blank=True, null=True)
    groups = models.ManyToManyField("Group", blank=True)

    def __str__(self):
        return str(self.email)


class Department(BaseModel):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.company} - {self.name}"


class Group(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)
