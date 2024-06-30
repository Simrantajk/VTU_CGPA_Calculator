from django.db import models

class Scheme(models.Model):
    scheme_id = models.AutoField(primary_key=True)
    scheme = models.IntegerField()

    def __str__(self):
        return f"Scheme {self.scheme}"

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, default='ISE')  # Default code
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, default=1)  # Default scheme_id

    def __str__(self):
        return f"{self.name} ({self.code})"

class Sem(models.Model):
    sem_id = models.AutoField(primary_key=True)
    sem = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)  # Default branch_id

    def __str__(self):
        return f"Sem {self.sem} - {self.branch.name}"

class Subject(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_code = models.CharField(max_length=255)
    sub_name = models.CharField(max_length=255)
    credits = models.IntegerField()
    max_marks = models.IntegerField()
    sem = models.ForeignKey(Sem, on_delete=models.CASCADE, default=1)  # Default sem_id

    def __str__(self):
        return f"{self.sub_name} ({self.sub_code})"
