from django.db import models
from django.contrib.auth.models import User


class WorkerType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % self.name


class Worker(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(WorkerType, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.type, self.name.username)


class Task(models.Model):
    person_name = models.ForeignKey(User, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=30)
    description = models.CharField(max_length=140)
    address = models.CharField(max_length=50)
    is_completed = models.BooleanField()

    def __str__(self):
        return "Task %s: %s for %s at %s: %s" % (
            str(self.id),
            self.short_name,
            self.person_name,
            self.address,
            self.description)


class Brigade(models.Model):
    member1 = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='member1')
    member2 = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='member2')
    member3 = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='member3')

    def __str__(self):
        return "Brigade %s: %s, %s, %s" % (str(self.id), self.member1, self.member2, self.member3)


class WorkPlan(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    brigade = models. ForeignKey(Brigade, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return "Task %s is assigned to brigade %s, it will be completed on %s" % (
            str(self.task.id),
            str(self.brigade.id),
            str(self.date)
        )


class Record(models.Model):
    username = models.ForeignKey(User)
    time = models.DateTimeField()

    def __str__(self):
        return "User " + self.username.username + " logged in at " + str(self.time)
