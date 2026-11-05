import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from preflight import check_name, check_project  # noqa: E402


def make(files: dict[str, str]) -> pathlib.Path:
    root = pathlib.Path(tempfile.mkdtemp(prefix="my-app-"))
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


PKG = '{"scripts": {"start": "node server.js"}}'
GOOD_NODE = "const port = process.env.PORT || 8080;\nrequire('http').createServer(() => {}).listen(port, '0.0.0.0');\n"


class ProjectTests(unittest.TestCase):
    def test_clean_project_passes(self):
        root = make({"package.json": '{"scripts": {"start": "node server.js"}}', "server.js": GOOD_NODE})
        self.assertEqual(check_project(root, "my-app"), ([], []))

    def test_missing_manifest(self):
        root = make({"server.js": GOOD_NODE})
        errors, _ = check_project(root, "my-app")
        self.assertTrue(any("no manifest" in e for e in errors))

    def test_server_must_read_port_and_not_bind_localhost(self):
        root = make({"package.json": "{}", "server.js": "require('http').createServer(() => {}).listen(3000, 'localhost');\n"})
        errors, _ = check_project(root, "my-app")
        self.assertTrue(any("PORT" in e for e in errors))
        self.assertTrue(any("localhost" in e for e in errors))

    def test_env_file_and_private_key_are_flagged(self):
        root = make({"package.json": "{}", ".env": "A=1", "key.pem": "x", "app.js": "const k='" + "-----BEGIN " + "RSA PRIVATE KEY-----" + "';"})
        errors, _ = check_project(root, "my-app")
        self.assertGreaterEqual(len([e for e in errors if ".env" in e or "key.pem" in e]), 2)
        self.assertTrue(any("private key" in e for e in errors))

    def test_connection_string_and_inference_key_in_source(self):
        root = make({"package.json": "{}", "db.py": "URL='postgres://user:pass@host/db'\nKEY='" + "sk-" + "ss-" + "x" * 16 + "'\n"})
        errors, _ = check_project(root, "my-app")
        self.assertTrue(any("connection string" in e for e in errors))
        self.assertTrue(any("inference API key" in e for e in errors))

    def test_dependency_folders_are_ignored(self):
        root = make({"package.json": PKG, "node_modules/x/.env": "A=1"})
        self.assertEqual(check_project(root, "my-app"), ([], []))

    def test_test_files_are_not_checked_for_ports(self):
        root = make({"package.json": PKG, "test.js": "server.listen(0, '127.0.0.1');\n"})
        self.assertEqual(check_project(root, "my-app"), ([], []))

    def test_package_json_without_start_is_a_warning(self):
        root = make({"package.json": '{"scripts": {}}'})
        _, warnings = check_project(root, "my-app")
        self.assertTrue(any("start" in w for w in warnings))


class NameTests(unittest.TestCase):
    def test_period_is_an_error(self):
        self.assertTrue(check_name("my.app", None)[0])

    def test_uppercase_is_normalized_with_a_warning(self):
        errors, warnings = check_name("My_App", None)
        self.assertEqual(errors, [])
        self.assertTrue(any("my-app" in w for w in warnings))

    def test_combined_label_over_63_is_an_error(self):
        errors, _ = check_name("a" * 60, "12345")
        self.assertTrue(any("63" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
