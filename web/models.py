from django.contrib.auth.models import User
from django.db import models


class House(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Alumnum(models.Model):
    user = models.OneToOneField(User, related_name="alumnum", on_delete=models.CASCADE)
    mobile = models.CharField(max_length=17)
    telephone = models.CharField(max_length=17, blank=True)
    whatsapp = models.CharField(max_length=17, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    year_of_completion = models.IntegerField()
    exam_type = models.CharField(max_length=20) # o/a level, sss, wassce
    house = models.ForeignKey(House, related_name="alumni", on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name="alumni", on_delete=models.CASCADE)
    member_id = models.CharField(max_length=20)
    profession = models.CharField(max_length=100)
    nickname = models.CharField(max_length=70, blank=True)

    reference_1 = models.TextField(blank=True)
    reference_2 = models.TextField(blank=True)
    
    verified = models.BooleanField(default=False)
    executive = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Alumni"

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if not self.member_id:
            code_number = str(len(Alumnum.objects.all())+1).rjust(4, '0')
            self.member_id = "%s%s" % (self.chapter.code, code_number)

        super(Alumnum, self).save(*args, **kwargs)


class Dues(models.Model):
    alumnum = models.ForeignKey(Alumnum, related_name="dues", on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now=True)
    for_how_many_months = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField(default=2018)

    class Meta:
        verbose_name_plural = "Dues"
        ordering = ('-date_paid', )


class Job(models.Model):
    post_title = models.CharField(max_length=70)
    position = models.CharField(max_length=70)
    short_description = models.CharField(max_length=250)
    job_description = models.TextField()
    salary_range = models.CharField(max_length=60)
    location = models.CharField(max_length=70)
    company = models.CharField(max_length=70)
    how_to_apply = models.CharField(max_length=70)
    date_added = models.DateTimeField(auto_now_add=True)
    qualifications = models.CharField(max_length=100)
    deadline = models.DateField()
    profession_type = models.CharField(max_length=100, default="General")
    posted_by = models.ForeignKey(Alumnum, related_name="jobs", on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date_added', )

    def __str__(self):
        return self.post_title


class Scholarship(models.Model):
    posted_by = models.ForeignKey(Alumnum, related_name="scholarships", on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    school = models.CharField(max_length=70)
    description = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    how_to_apply = models.CharField(max_length=70)

    def __str__(self):
        return self.title


class ProjectType(models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    target = models.DecimalField(decimal_places=2, max_digits=10)
    payment_deadline = models.DateField()
    least_contribution = models.DecimalField(decimal_places=2, max_digits=6)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    project_type = models.ForeignKey(ProjectType, related_name="project", on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to="images/", blank=True)
    image2 = models.ImageField(upload_to="images/", blank=True)
    image3 = models.ImageField(upload_to="images/", blank=True)
    image4 = models.ImageField(upload_to="images/", blank=True)
    image5 = models.ImageField(upload_to="images/", blank=True)
    image6 = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        ordering = ('-date_created', )

    
    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    guests = models.CharField(max_length=300, blank=True)
    rate = models.DecimalField(default=0.0, decimal_places=2, max_digits=9)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    


