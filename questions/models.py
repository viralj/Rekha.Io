from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


# Create your models here.
from common.models import Tag


class Question(models.Model):
    """
    Question model to store question from user.
    """
    title = models.CharField(_('question title or short question'), max_length=250)
    details = models.TextField(_('question details'))
    created_by = models.ForeignKey('accounts.User')
    is_archived = models.BooleanField(_('is this question archived?'), default=False)
    date_created = models.DateTimeField(_('date question created'), default=timezone.now)
    last_modified = models.DateTimeField(_('date question modified'), default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='questions')


class Comments(models.Model):
    """
    Comments model for comments posted for question.
    """
    belongs_to_question = models.ForeignKey('questions.Question')
    comment = models.TextField(_('comment'), max_length=500)
    created_by = models.ForeignKey('accounts.User')
    is_archived = models.BooleanField(_('is this comment archived?'), default=False)
    date_created = models.DateTimeField(_('date comment created'), default=timezone.now)
    last_modified = models.DateTimeField(_('date comment modified'), default=timezone.now)


class Answers(models.Model):
    """
    Answers model for answers posted for question.
    """
    belongs_to_question = models.ForeignKey('questions.Question')
    answer = models.TextField(_('answer'))
    created_by = models.ForeignKey('accounts.User')
    is_archived = models.BooleanField(_('is this answer archived?'), default=False)
    date_created = models.DateTimeField(_('date answer created'), default=timezone.now)
    last_modified = models.DateTimeField(_('date answer modified'), default=timezone.now)


class VotesQ(models.Model):
    """
    Votes for Questions
    """
    belongs_to_question = models.ForeignKey('questions.Question')
    vote_type = models.IntegerField(_('positive or negative vote'))
    created_by = models.ForeignKey('accounts.User')
    date_created = models.DateTimeField(_('date vote created'), default=timezone.now)
    last_modified = models.DateTimeField(_('date vote modified'), default=timezone.now)


class VotesC(models.Model):
    """
    Votes for Comments
    """
    belongs_to_comment = models.ForeignKey('questions.Comments')
    vote_type = models.IntegerField(_('positive or negative vote'))
    created_by = models.ForeignKey('accounts.User')
    date_created = models.DateTimeField(_('date vote created'), default=timezone.now)
    last_modified = models.DateTimeField(_('date vote modified'), default=timezone.now)


class VotesA(models.Model):
    """
    Votes for Answers
    """
    belongs_to_answer = models.ForeignKey('questions.Answers')
    vote_type = models.IntegerField(_('positive or negative vote'))
    created_by = models.ForeignKey('accounts.User')
    date_created = models.DateTimeField(_('date vote created'), default=timezone.now)
    last_modified = models.DateTimeField(_('date vote modified'), default=timezone.now)
