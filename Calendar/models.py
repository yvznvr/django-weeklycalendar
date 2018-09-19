from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

REPEAT_FREQ = (
    ('1', "Day"),
    ('2', "Week"),
    ('3', "Month"),
    ('4', "Year")
)

COLORS = [
    ('#eeeeee', 'gray'),
    ('#ff0000', 'red'),
    ('#0000ff', 'blue'),
    ('#00ff00', 'green'),
    ('#000000', 'black'),
    ('#ffffff', 'white'),
    ('#7E8F7C', 'khaki'),
]

class Activity(models.Model):
    title = models.CharField(verbose_name="Title", max_length=50)
    date = models.DateField(verbose_name="Date")
    start_time = models.TimeField(verbose_name="Start Time")
    finish_time = models.TimeField(verbose_name="Finish Time")
    repeat_fre = models.CharField(verbose_name="Repeat Frequency", max_length=50, choices=REPEAT_FREQ, blank=True)
    repeat_time = models.PositiveIntegerField(verbose_name="Repeat Time", validators=[MaxValueValidator(20)], blank=True, null=True)
    location = models.CharField(verbose_name="Location", max_length=50, blank=True, null=True)
    color = models.CharField(verbose_name="Color", max_length=7, choices=COLORS, default="gray")
    private = models.BooleanField(verbose_name="Private", default=False)
    comment = models.TextField(verbose_name="Comment", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_activity = models.ManyToManyField('Activity', verbose_name="Related Activities", blank=True)

    def __str__(self):
        return self.title + " " + str(self.start_time) + "-" + str(self.finish_time)

    def save(self, *args, **kwargs):
        if(self.id != None):
            for i in self.related_activity.all():
                i.delete()

        if(self.repeat_fre == ''):
            return super().save(*args, **kwargs)
        super().save(*args, **kwargs)
        obj = Activity.objects.get(id=self.id)
        obj.repeat_time = 0
        obj.repeat_fre = 0
        for i in range(1,int(self.repeat_time)):
            obj.id = None;
            if (self.repeat_fre == "1"):    #day
                date = self.date + relativedelta(days=i)
            elif (self.repeat_fre == "2"):  #week
                date = self.date + relativedelta(days=7*i)
            elif (self.repeat_fre == "3"):  #month
                date = self.date + relativedelta(months=i)
            else:                           #year
                date = self.date + relativedelta(years=i)
            obj.date = date
            obj.save()
            # Following line does not work on admin panel bacause of
            # https://stackoverflow.com/questions/1925383/issue-with-manytomany-relationships-not-updating-immediately-after-save/1925784#1925784
            self.related_activity.add(obj)

    def delete(self, using=None, keep_parents=False):
        # if there are related activities
        if(self.related_activity.count()):
            for i in self.related_activity.all():
                i.delete()
            return super().delete()
        return  super().delete()


    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
