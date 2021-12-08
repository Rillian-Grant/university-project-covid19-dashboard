import unittest

import sched
import threading
import random

from covid19_dashboard.data_handler import BackgroundDataUpdateHandler, DataUpdate

class TestBackgroundDataUpdateHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._data_handler = BackgroundDataUpdateHandler()

    def test_set_up_correctly(self):
        self.assertIsInstance(self._data_handler, BackgroundDataUpdateHandler)
        self.assertIsInstance(self._data_handler.scheduler_instance, sched.scheduler)
        self.assertIsInstance(self._data_handler.background_thread_instance, threading.Thread)

        self.assertTrue(self._data_handler.background_thread_instance.is_alive())

    def test_schedule_data_update(self):
        data_update = DataUpdate(
            interval=1,
            label="Test Update",
            repeat=False,
        )

        self._data_handler.schedule(data_update)

        self.assertIsInstance(self._data_handler.scheduled_events[0], DataUpdate)

    def test_remove_data_update(self):
        data_update = DataUpdate(
            interval=1,
            label="Test Update",
            repeat=False,
        )

        before_len = len(self._data_handler.scheduled_events)

        self._data_handler.schedule(data_update)

        self._data_handler.remove(data_update)

        self.assertEqual(len(self._data_handler.scheduled_events), before_len)

    def test_remove_news_articles(self):
        article = random.choice(self._data_handler.dashboard_data()["news_articles"])
        
        self._data_handler.remove_news_article(article["title"])

        self.assertTrue(
            article not in self._data_handler.dashboard_data()["news_articles"]
        )