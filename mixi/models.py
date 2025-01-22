from django.db import models



class Note(models.Model):
    email = models.CharField(verbose_name="Email", max_length=50)
    note = models.CharField(verbose_name="Note", max_length=255)

    def __str__(self):
        return f"{self.email} - {self.note}"

class Task(models.Model):
    email = models.CharField(verbose_name="Email", max_length=50)
    task = models.CharField(verbose_name="Task", max_length=255)
    complete = models.BooleanField(verbose_name="Complete", default=False)

    def __str__(self):
        return f"{self.email} - {self.task}- {self.complete}"

class Shortcut(models.Model):
    email = models.CharField(verbose_name="Email", max_length=50)
    name = models.CharField(verbose_name="Name", max_length=255)
    url = models.CharField(verbose_name="Url", max_length=255)

    def __str__(self):
        return f"{self.email} - {self.name} - {self.url}"

class Alarm(models.Model):
    email = models.CharField(verbose_name="Email", max_length=50)
    name = models.CharField(verbose_name="Alarm Name", max_length=100)
    time = models.TimeField(verbose_name="Alarm Time")
    additional_info = models.TextField(verbose_name="Additional Info", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)

    def __str__(self):
        return f"{self.name} - {self.time}"

class Image(models.Model):
    email = models.CharField(verbose_name="Email", max_length=50)
    image = models.FileField(verbose_name="Alarm Name", upload_to="mixifind/")

    def __str__(self):
        return f"{self.image}"

class Sponsor(models.Model):
    name = models.CharField(verbose_name="Sponsor Name", max_length=100)
    number = models.PositiveNumber(verbose_name="Location Number")
    code = models.TextField(verbose_name="Iframe Code")
    is_active = models.BooleanField(verbose_name="Active", default=True)

    def __str__(self):
        return f"{self.name} - {self.is_active}"
        
class Quote(models.Model):
    email = models.CharField(verbose_name="Email", max_length=50)
    quote = models.CharField(verbose_name="Quote", max_length=255)

    def __str__(self):
        return f"{self.email} - {self.quote}"
        

        
        
        
        
        
