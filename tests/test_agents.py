import unittest
from src.core.agents import pick_agent_name

class TestAgents(unittest.TestCase):
    def test_agent_name_unique(self):
        used = set()
        name1 = pick_agent_name(used)
        used.add(name1)
        name2 = pick_agent_name(used)
        self.assertNotEqual(name1, name2)

if __name__ == "__main__":
    unittest.main()
