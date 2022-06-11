from django.conf import settings
from django.db import models


class Project(models.Model):
    """ Project Information """

    PROJECT_TYPE = [
        ("back-end", "Back-End"),
        ("front-end", "Front-End"),
        ("ios", "iOS"),
        ("android", "Android")
    ]

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    date_updated = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=128, verbose_name="Title")
    description = models.CharField(max_length=2048, verbose_name="Description")
    type = models.CharField(max_length=15, choices=PROJECT_TYPE, verbose_name="Type")
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='projects',
                                    verbose_name="Project author",
                                    null=True)

    def __str__(self):
        return f"{self.title}"


class Contributor(models.Model):
    """ Relations between users and projects """

    ROLE_CHOICES = [
        ("author", "Author"),
        ("contributor", "Contributor")
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="contributors"
                             )
    project = models.ForeignKey(to=Project,
                                on_delete=models.CASCADE,
                                related_name="project_contributor"
                                )
    role = models.CharField(max_length=128, choices=ROLE_CHOICES, verbose_name="Roles")

    def __str__(self):
        return f"{self.user}"


class Issue(models.Model):
    """ all information relating to an issue """

    TAG_CHOICES = [
        ("bug", "Bug"),
        ("improvement", "Improvement"),
        ("task", 'Task')
    ]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ]
    STATUS_CHOICES = [
        ("todo", "To do"),
        ("in progress", "In progress"),
        ("completed", "Completed")
    ]

    title = models.CharField(max_length=128, verbose_name="Title")
    description = models.CharField(max_length=2048, verbose_name="Description")
    tag = models.CharField(max_length=128, choices=TAG_CHOICES)
    priority = models.CharField(max_length=128, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(to=Project,
                                on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='issues_author')
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      default=author_user,
                                      related_name='issues_assigned')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    """ comment of a particular issue """

    description = models.CharField(max_length=2048, verbose_name="Description")
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='comment_author')
    issue = models.ForeignKey(to=Issue,
                              on_delete=models.CASCADE,
                              related_name='comment_issue')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    def __str__(self):
        return f"Comment from issue - {self.issue} -"
