from django.db import models


class Employee(models.Model):
    employeeId = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    roleType = models.CharField(max_length=50)
    teamId = models.ForeignKey("Team", on_delete=models.CASCADE())

    def __str__(self):
        return self.firstname + " " + self.lastname


class Team(models.Model):
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=50)
    departmentId = models.ForeignKey("Department", on_delete=models.CASCADE())


class EmployeeTeams(models.Model):
    teamId = models.ForeignKey(Team, on_delete=models.CASCADE())
    employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE())

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["teamId", "employeeId"], name="unique_employee_team")
        ]


class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=50)


class HealthCheckType(models.Model):
    typeId = models.AutoField(primary_key=True)
    displayName = models.CharField(max_length=50)


class HealthCheck(models.Model):
    checkId = models.AutoField(primary_key=True)
    #     composite key from employee teams
    teamId = models.ForeignKey(Team, on_delete=models.CASCADE())
    employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE())
    timestamp = models.DateTimeField(auto_now_add=True)


class HealthCheckVotes(models.Model):
    checkId = models.ForeignKey(HealthCheck, on_delete=models.CASCADE())
    typeId = models.ForeignKey(HealthCheckType, on_delete=models.CASCADE())
    vote = models.CharField(max_length=50)
    direction = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["checkId", "typeId"], name="unique_vote")
        ]
