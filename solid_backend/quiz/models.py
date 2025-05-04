from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from taggit.managers import TaggableManager
from taggit.models import TaggedItem


class QuizQuestion(models.Model):
    """
    Model for a quesiton in the quiz of the app.
    """

    QTYPE_CHOICES = [
        ("SC", "Single Choice"),
        ("MC", "Multiple Choice"),
        ("DD", "Drag and Drop"),
        ("TF", "True or False"),
        ("RN", "Range"),
        ("RG", "Ranking"),
        ("HS", "Hotspot"),
    ]
    QDIFFICULTY_CHOICES = [
        (1, "Neuling"),
        (2, "Einsteiger"),
        (3, "Fortgeschrittener"),
        (4, "Erfahrener"),
        (5, "Experte"),
    ]

    type = models.CharField(max_length=2, choices=QTYPE_CHOICES)
    difficulty = models.PositiveSmallIntegerField(choices=QDIFFICULTY_CHOICES)
    text = models.TextField(verbose_name="text (Markdown)")
    img = GenericRelation(to="media_object.MediaObject")
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.text


class QuizAnswer(models.Model):
    """
    Model for an answer to a question of the QuizQuestion model.
    """

    question = models.ForeignKey(
        to=QuizQuestion,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
    )
    text = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="text (Markdown)"
    )
    correct = models.BooleanField(
        null=True,
        blank=True,
    )
    feedback_correct = models.CharField(max_length=400, null=True, blank=True)
    feedback_incorrect = models.CharField(max_length=400, null=True, blank=True)

    ranking_position = models.IntegerField(null=True, blank=True)
    subsequences = models.BooleanField(null=True, blank=True)
    feedback_subsequences = models.CharField(max_length=400, blank=True, null=True)

    range_value = models.FloatField(null=True, blank=True)
    range_max = models.FloatField(null=True, blank=True)
    range_min = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=400, null=True, blank=True)
    range_step = models.FloatField(null=True, blank=True)
    tolerance = models.FloatField(null=True, blank=True)


@receiver(post_delete, sender=TaggedItem)
def delete_orphaned_tags(sender, instance, **kwargs):
    n_tagged = TaggedItem.objects.filter(tag_id=instance.tag_id).count()
    if n_tagged == 0:
        instance.tag.delete()
