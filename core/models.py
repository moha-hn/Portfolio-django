from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500)
    url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',')]

    def __str__(self):
        return self.title


class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    year_start = models.CharField(max_length=10)
    year_end = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.degree} – {self.institution}"


class Talk(models.Model):
    title = models.CharField(max_length=300)
    event = models.CharField(max_length=200)
    date = models.CharField(max_length=50)
    description = models.TextField()
    linkedin_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='talks/', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title