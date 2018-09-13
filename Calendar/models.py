from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


REPEAT_FREQ = (
    (1, "Day"),
    (2, "Week"),
    (3, "Month"),
    (4, "Year")
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

    def __str__(self):
        return self.title + " " + str(self.start_time) + "-" + str(self.finish_time)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
