from django.contrib import admin
from app.models import WorkPlan, Brigade, Worker, WorkerType, Record


@admin.register(WorkerType)
class WorkerTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass


@admin.register(Brigade)
class BrigadeAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkPlan)
class WorkPlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass
