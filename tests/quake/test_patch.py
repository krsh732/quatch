import unittest
from . import run_quake
from quatch import Qvm


class TestPatch(unittest.TestCase):
    def test_patch(self):
        symbols = {
            "G_InitGame": 0x2B7,
            "Com_Printf": 0x446,
        }

        qvm = Qvm("defrag/vm/original_qagame.qvm", symbols=symbols)
        qvm.add_c_code(
            r"""
            void G_InitGame(int levelTime, int randomSeed, int restart);
            void Com_Printf(const char *fmt, ...);

            void G_InitGame_hook(int levelTime, int randomSeed, int restart) {
                Com_Printf("\nQUATCH: Hooked\n");
                G_InitGame(levelTime, randomSeed, restart);
            }
            """
        )
        qvm.replace_calls("G_InitGame", "G_InitGame_hook")
        qvm.write("defrag/vm/qagame.qvm")

        output = run_quake().decode()
        self.assertTrue("QUATCH: Hooked" in output.splitlines())
