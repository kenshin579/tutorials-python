from unittest import TestCase

from kakao.second_half.caching import solution


class TestSolution(TestCase):
    def test_get_solution1(self):
        self.assertEquals(50, solution(3, ["Jeju", "Pangyo", "Seoul", "NewYork", "LA", "Jeju", "Pangyo", "Seoul", "NewYork", "LA"]))
        self.assertEqual(21, solution(3, ["Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul"]))
        self.assertEqual(45, solution(0, ["Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul"]))