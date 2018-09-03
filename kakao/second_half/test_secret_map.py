import time
from unittest import TestCase

from kakao.second_half.secret_map import solution


class TestSolution(TestCase):
    def test_get_solution(self):
        start_time = time.time()
        result = solution(5, [9, 20, 28, 18, 11],
                          [30, 1, 21, 17, 28])
        print("--- %s seconds ---" % (time.time() - start_time))

        self.assertEquals(["#####", "# # #", "### #", "#  ##", "#####"], result)
