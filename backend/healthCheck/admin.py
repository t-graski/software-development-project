from django.contrib import admin

from .models import HealthCheck, Department, Employee, EmployeeTeams, HealthCheckType, HealthCheckVotes, Team

admin.site.register(HealthCheck)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(EmployeeTeams)
admin.site.register(HealthCheckType)
admin.site.register(HealthCheckVotes)
admin.site.register(Team)
