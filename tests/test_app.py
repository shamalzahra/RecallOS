import sys, unittest, tempfile, unittest.mock
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app
class TestRecall(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();app.DB=Path(cls.tmp.name)/'test.db';app.init()
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_seeded(self):self.assertGreaterEqual(len(app.topics()),6)
 def test_retention(self):self.assertTrue(all(0<=x['retention']<=100 for x in app.topics()))
 def test_agent(self):self.assertEqual(app.agent('What am I forgetting?')['tool'],'get_memory_risk')
 def test_quiz(self):
  x=app.topics()[0];d=app.answer(x['id'],x['answer']);self.assertTrue(d['correct']);self.assertGreater(app.state()['stats']['quiz_attempts'],0)
 def test_import_notes(self):
  result=app.import_notes("Biology","Mitosis: A type of cell division producing two genetically identical daughter cells.\nOsmosis: Movement of water through a semipermeable membrane from low solute concentration toward higher solute concentration.")
  self.assertEqual(result["count"],2)
  imported=next(x for x in app.topics() if x["name"]=="Mitosis")
  self.assertIn("cell division",app.reveal(imported["id"])["reference_answer"])
 def test_reject_invalid_notes(self):
  with self.assertRaises(ValueError):app.import_notes("Test","hello")
 def test_tool_call(self):
  result=app.execute_agent_tool("build_revision_plan",{})
  self.assertEqual(result["action"],"show_plan")
  self.assertIn("retention",result["reply"])
 def test_tool_rejected(self):
  with self.assertRaises(ValueError):app.execute_agent_tool("delete_all_topics",{})
 def test_offline_smart_agent(self):
  with unittest.mock.patch.dict("os.environ",{"RECALLOS_API_KEY":""}):
   self.assertEqual(app.smart_agent("Quiz me")["mode"],"offline")
 def test_wrong_choice(self):
  with self.assertRaises(ValueError):app.answer(1,200)
if __name__=='__main__':unittest.main()
