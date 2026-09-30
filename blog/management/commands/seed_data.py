from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post


class Command(BaseCommand):
    help = "Create dummy blog data"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@example.com"
            }
        )

        posts = [
            {
                "title": "Getting Started with Django",
                "content": "Django is a powerful Python web framework for building secure and scalable web applications.",
            },
            {
                "title": "Building APIs with Django REST Framework",
                "content": "Django REST Framework makes it easy to build powerful and scalable APIs for web and mobile applications.",
            },
            {
                "title": "Deploying Django on Render",
                "content": "Render provides a simple way to deploy Django applications and make them available online.",
            },
            {
                "title": "Understanding Django Models",
                "content": "Django models help developers define database structures using Python classes and make database operations easier.",
            },
            {
                "title": "Working with PostgreSQL in Django",
                "content": "PostgreSQL is a powerful relational database that works well with Django applications and supports complex queries.",
            },
            {
                "title": "Introduction to Python Web Development",
                "content": "Python provides several frameworks and tools that make web development faster, easier, and more maintainable.",
            },
            {
                "title": "Authentication in Django",
                "content": "Django includes a built-in authentication system for managing users, passwords, permissions, and sessions.",
            },
            {
                "title": "Building Better Web Applications",
                "content": "A good web application should be secure, maintainable, responsive, and easy for users to navigate.",
            },
        ]

        for post in posts:
            Post.objects.get_or_create(
                title=post["title"],
                defaults={
                    "content": post["content"],
                    "author": user,
                }
            )

        self.stdout.write(
            self.style.SUCCESS("Dummy data created successfully.")
        )
