from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Source: https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    # Source: https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
    class Meta:
        unique_together= ('user_id', 'following_user_id')
        ordering = ["-timestamp"]

    def __str__(self):
        f"{self.user_id} follows {self.following_user_id}"

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    comments = models.ForeignKey("Comment", null=True, on_delete=models.CASCADE, related_name="comments")
    likes = models.ForeignKey("Like", null=True, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment = models.TextField(blank=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_comments")
    timestamp = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_likes")
    timestamp = models.DateTimeField(auto_now_add=True)