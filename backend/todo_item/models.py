from uuid import uuid4
from django.db import models
from channels.binding.websockets import WebsocketBinding


class TodoList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=140)

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    todo_list = models.ForeignKey(TodoList, related_name="todo_items", null=True)
    title = models.CharField(max_length=140, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TodoItemBinding(WebsocketBinding):
    model = TodoItem
    stream = "todo_item"
    fields = ("title", "status", "todo_list",)

    @classmethod
    def group_names(cls, instance):
        list_id = str(instance.todo_list.id)
        return (list_id,)

    @classmethod
    def has_permission(self, user, action, pk):
        # CRUD just trough REST API
        return False
