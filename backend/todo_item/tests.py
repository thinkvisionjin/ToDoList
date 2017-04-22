from django.test import TestCase
from channels.test import ChannelTestCase, HttpClient

from .models import TodoItem, TodoList


class TodoListTests(TestCase):
    def test_can_have_todo_items_in_todo_list(self):
        todo_list = TodoList.objects.create(title='default')
        TodoItem.objects.create(title='brush teeth', todo_list=todo_list)

    def test_when_add_new_todo_items_it_adding_to_todo_list(self):
        qty_todo_lists_before = TodoList.objects.count()
        payload = {'title': 'Brush teeth'}
        response = self.client.post('/api/web/todo_item/', payload)
        self.assertEqual(response.status_code, 201)

        self.assertTrue(TodoList.objects.filter(id=response.json()['todo_list']).exists())
        self.assertEqual(TodoList.objects.count(), qty_todo_lists_before + 1)

    def test_can_create_many_todo_lists_but_cant_look_at_them_without_direct_link(self):
        qty_todo_items_before = TodoList.objects.count()
        payload = {'title': 'Homework'}
        response = self.client.post('/api/web/todo_list/', payload)
        self.assertEqual(response.status_code, 201)
        payload = {'title': 'Products'}
        response = self.client.post('/api/web/todo_list/', payload)
        self.assertEqual(response.status_code, 201)

        # todo_lists must exists in db
        self.assertEqual(TodoList.objects.count(), qty_todo_items_before + 2)

        response = self.client.get('/api/web/todo_item/')
        self.assertEqual(len(response.json()), 0)

    def test_can_get_access_to_todo_list_by_direct_link(self):
        qty_todo_items_before = TodoList.objects.count()
        payload = {'title': 'Homework'}
        response = self.client.post('/api/web/todo_list/', payload)
        self.assertEqual(response.status_code, 201)

        # todo_list must exists in db
        self.assertEqual(TodoList.objects.count(), qty_todo_items_before + 1)

        todo_list_uid = response.json()['id']
        # unique id of list must be very long
        self.assertTrue(len(todo_list_uid) > 10)

        response = self.client.get('/api/web/todo_list/{}/'.format(todo_list_uid))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['title'], 'Homework')

    def test_can_see_all_todo_items_directed_to_special_list(self):
        todo_list1 = TodoList.objects.create(title="Homework")
        todo_list2 = TodoList.objects.create(title="Products")
        todo_item1 = TodoItem.objects.create(todo_list=todo_list1, title="Buy products")
        todo_item2 = TodoItem.objects.create(todo_list=todo_list2, title="Bread")
        todo_item3 = TodoItem.objects.create(todo_list=todo_list2, title="Rice")

        # can't get all todo_items by one request
        response = self.client.get('/api/web/todo_item/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        # can get filtered todo_items by todo_list
        response = self.client.get('/api/web/todo_item/', {'todo_list': todo_list2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertNotContains(response, todo_item1)
        self.assertContains(response, todo_item2)
        self.assertContains(response, todo_item3)


class WebSocketTests(ChannelTestCase):
    def test_creating_new_todo_items_send_notification(self):
        client = HttpClient()
        client.join_group("todo_list")

        TodoItem.objects.create(title="test_item")

        received = client.receive()

        self.assertNotEquals(received, None)

    def test_cant_add_new_todo_item_by_ws(self):
        client = HttpClient()
        client.join_group("todo_list")

        payload = {
            'stream': 'todo_item',
            'payload': {'data': {'title': 'test_item'}, 'action': 'create',}
        }

        client.send_and_consume('websocket.receive', path='/api/ws/', text=payload)

        self.assertEqual(TodoItem.objects.count(), 0)
