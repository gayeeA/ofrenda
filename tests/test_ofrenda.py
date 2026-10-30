import os, tempfile, unittest
os.environ["OFRENDA_HOME"] = tempfile.mkdtemp()
from ofrenda import store, memory, render, llm


class T(unittest.TestCase):
    def setUp(self):
        llm.chat = lambda system, user, temperature=0.4: "STUB<" + user[-60:] + ">"
        llm.embed = lambda texts: None  # force keyword fallback
        store.add_person("Abuela Rosa", "1931", "2019", ["tamales"], ["Cielito Lindo"], ["rebozo"])
        store.add_story("abuela-rosa", "She made tamales every December and sang while stirring the masa.", teller="Mom")
        store.add_story("abuela-rosa", "She walked to the market at dawn with her blue rebozo.")

    def test_slug(self):
        self.assertEqual(store.slugify("Tío José Ñ"), "tio-jose-n")

    def test_retrieval_picks_relevant(self):
        top = memory.retrieve("abuela-rosa", "what did she cook at christmas tamales?", k=1)
        self.assertIn("tamales", top[0]["text"])

    def test_ask_and_remember(self):
        self.assertTrue(memory.ask("abuela-rosa", "tamales?").startswith("STUB"))
        self.assertTrue(memory.remember("abuela-rosa").startswith("STUB"))

    def test_render_escapes_and_offline(self):
        store.add_story("abuela-rosa", "<script>alert(1)</script>")
        out = render.build(out=os.path.join(os.environ["OFRENDA_HOME"], "o.html"))
        h = open(out, encoding="utf-8").read()
        self.assertNotIn("<script>alert", h)
        self.assertNotIn("http://", h.replace("http://www.w3.org", ""))
        self.assertNotIn("https://", h)
        self.assertIn("Abuela Rosa", h)

if __name__ == "__main__":
    unittest.main()
