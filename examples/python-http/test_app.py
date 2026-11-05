import json
import threading
import unittest
from urllib.request import urlopen

from app import make_server


class AppTests(unittest.TestCase):
    def setUp(self):
        self.server = make_server(0, "127.0.0.1")
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_health_check(self):
        with urlopen(f"http://127.0.0.1:{self.port}/healthz") as res:
            self.assertEqual(json.load(res), {"status": "ok"})

    def test_home_page(self):
        with urlopen(f"http://127.0.0.1:{self.port}/") as res:
            self.assertIn("Internal app", res.read().decode())


if __name__ == "__main__":
    unittest.main()
