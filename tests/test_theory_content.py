import importlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]


class TheoryContentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.previous_env = {key: os.environ.get(key) for key in ("DB_PATH", "DATABASE_URL")}
        os.environ["DB_PATH"] = str(Path(cls.temporary.name) / "theory.db")
        # Estes testes só leem conteúdo: nunca abrem o banco real da DATABASE_URL.
        os.environ.pop("DATABASE_URL", None)
        sys.path.insert(0, str(PROJECT))
        cls.site = importlib.import_module("app")

        from backend.conteudo.exemplos_teoricos import ARQUIVOS_BUILD
        from backend.conteudo.teoria_ampliada import LEITURAS
        from backend.conteudo.trilha import MODULOS

        cls.MODULOS = MODULOS
        cls.LEITURAS = LEITURAS
        cls.ARQUIVOS_BUILD = ARQUIVOS_BUILD
        cls.lessons = [lesson for module in MODULOS for lesson in module["licoes"]]

    @classmethod
    def tearDownClass(cls):
        sys.modules.pop("app", None)
        sys.path.remove(str(PROJECT))
        for key, value in cls.previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        cls.temporary.cleanup()

    def test_all_lessons_have_specific_readings(self):
        self.assertEqual(len(self.lessons), 91)
        self.assertEqual(set(self.LEITURAS), {lesson["titulo"] for lesson in self.lessons})
        self.assertEqual(len({lesson["leitura"]["explicacao"] for lesson in self.lessons}), 91)
        for lesson in self.lessons:
            with self.subTest(lesson=lesson["titulo"]):
                reading = lesson["leitura"]
                self.assertGreater(len(reading["explicacao"]), 200)
                self.assertGreaterEqual(len(reading["passos"]), 2)
                for key in ("objetivo", "aplicacao", "pergunta", "resposta"):
                    self.assertTrue(reading[key].strip())
                self.assertIn(lesson["exercicio_codigo"], lesson["pontos_chave"][1])
                self.assertEqual(lesson["desafios_teoricos"][2]["resposta"], lesson["exercicio_codigo"])

    def test_project_guides_have_valid_prerequisites(self):
        guides = [lesson for lesson in self.lessons if "guia_projeto" in lesson]
        self.assertEqual(len(guides), 7)
        lookup = {lesson["id"]: lesson for lesson in self.lessons}
        for lesson in guides:
            guide = lesson["guia_projeto"]
            self.assertGreaterEqual(len(guide["etapas"]), 4)
            self.assertGreaterEqual(len(guide["testes"]), 4)
            for prerequisite in guide["revisar"]:
                self.assertLess(prerequisite["id"], lesson["id"])
                self.assertEqual(lookup[prerequisite["id"]]["titulo"], prerequisite["titulo"])
                module = next(m for m in self.MODULOS if m["id"] == prerequisite["modulo_id"])
                self.assertIn(lookup[prerequisite["id"]], module["licoes"])

    def test_template_renders_all_lessons_without_changing_quiz_controls(self):
        from flask import render_template
        self.site.app.config["TESTING"] = True
        for module in self.MODULOS:
            for lesson in module["licoes"]:
                with self.subTest(lesson=lesson["titulo"]), self.site.app.test_request_context("/"):
                    html = render_template(
                        "estudo/estudar.html", modulo=module, licao=lesson,
                        concluidas_ids=[], favorita=False,
                        desafios_teoricos=lesson["desafios_teoricos"],
                        desafios_teoricos_corretos=0, total_desafios_teoricos=3,
                        anotacao="", posicao=module["licoes"].index(lesson) + 1,
                        anterior=None, proxima=None,
                    )
                    self.assertIn("Como funciona", html)
                    self.assertIn("Pense antes de continuar", html)
                    self.assertIn("Indo além", html)
                    self.assertEqual(html.count('class="quiz"'), 3)
                    self.assertEqual(html.count('data-desafio-id="'), 3)
                    self.assertNotIn("<stdio.h>", html)
                    self.assertIn("&lt;stdio.h&gt;", html)

    def compiler(self):
        compiler = os.environ.get("THEORY_CC") or shutil.which("gcc")
        if not compiler:
            self.skipTest("GCC indisponivel; defina THEORY_CC para testar os exemplos C11.")
        return compiler

    def compile(self, compiler, sources, executable, folder):
        environment = os.environ.copy()
        environment["PATH"] = str(Path(compiler).resolve().parent) + os.pathsep + environment.get("PATH", "")
        result = subprocess.run(
            [compiler, "-std=c11", "-Wall", "-Wextra", "-Werror", "-pedantic",
             *map(str, sources), "-lm", "-o", str(executable)],
            cwd=folder, capture_output=True, text=True, timeout=60, env=environment,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_compile_and_run_all_c_examples(self):
        compiler = self.compiler()
        for lesson in self.lessons:
            with self.subTest(lesson=lesson["titulo"]), tempfile.TemporaryDirectory() as folder:
                source = Path(folder) / "main.c"
                executable = Path(folder) / ("program.exe" if os.name == "nt" else "program")
                source.write_text(lesson["codigo"], encoding="utf-8")
                self.compile(compiler, [source], executable, folder)
                example = lesson.get("exemplo_execucao")
                cases = example["casos"] if example else [{"entrada": "Ana\n", "retorno": 0}]
                for case in cases:
                    with self.subTest(input=case["entrada"]):
                        result = subprocess.run(
                            [str(executable)], input=case["entrada"], cwd=folder,
                            capture_output=True, text=True, timeout=5,
                        )
                        self.assertEqual(result.returncode, case["retorno"], result.stderr)
                        if "saida" in case:
                            self.assertEqual(result.stdout, case["saida"])
                        else:
                            self.assertTrue(result.stdout.strip())

    def test_multifile_example_compiles_and_makefile_lists_dependencies(self):
        compiler = self.compiler()
        with tempfile.TemporaryDirectory() as folder:
            for file in self.ARQUIVOS_BUILD:
                (Path(folder) / file["nome"]).write_text(file["codigo"], encoding="utf-8")
            executable = Path(folder) / ("program.exe" if os.name == "nt" else "program")
            self.compile(compiler, ["main.c", "calculos.c"], executable, folder)
            result = subprocess.run([str(executable)], cwd=folder, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "42\n")
            makefile = (Path(folder) / "Makefile").read_text(encoding="utf-8")
            self.assertIn("main.o: main.c calculos.h", makefile)
            self.assertIn("calculos.o: calculos.c calculos.h", makefile)
            self.assertEqual(sum(line.startswith("\t") for line in makefile.splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
