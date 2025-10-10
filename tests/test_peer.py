import unittest
from src.core.agents import pick_agent_name

class TestPeer(unittest.TestCase):
    def test_agent_names_unique(self):
        """Stellt sicher, dass Agenten-Namen eindeutig zugewiesen werden"""
        used_names = set()
        name1 = pick_agent_name(used_names)
        used_names.add(name1)
        name2 = pick_agent_name(used_names)
        used_names.add(name2)
        self.assertNotEqual(name1, name2)
        self.assertTrue(name1.startswith("AGENT"))
        self.assertTrue(name2.startswith("AGENT"))

if __name__ == "__main__":
    unittest.main()
