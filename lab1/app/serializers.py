from rest_framework import serializers
from app.models import WorkerType, Worker, Task, Brigade, WorkPlan


class WorkerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerType
        fields = ('id', 'name')


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'name', 'type')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'person_name', 'short_name', 'description', 'address', 'is_completed')


class BrigadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brigade
        fields = ('id', 'member1', 'member2', 'member3')


class WorkPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlan
        fields = ('id', 'task', 'brigade', 'date')
