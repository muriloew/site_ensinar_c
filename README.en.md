# Ensinar C

🇺🇸 English | 🇧🇷 [Português](README.md)

Web platform for learning the C language: 21 modules and 91 lessons with theory, theory challenges, auto-graded exercises and a GCC compiler with an interactive terminal in the browser.

**Live:** https://site-ensinar-c-3.onrender.com

The change history of each version is in [`docs/historico-versoes.md`](docs/historico-versoes.md) (in Portuguese).

> The platform itself is in Portuguese, and so are the folder, file and function names in the code.

## Where everything lives

```txt
app.py                          Entry point: builds the site (Gunicorn uses app:app)
backend/
  banco/                        Database
    conexao.py                  Connection: PostgreSQL with DATABASE_URL, otherwise local SQLite
    tabelas.py                  Table creation and upgrade of older databases
  conteudo/                     What the student studies
    trilha.py                   The 21 modules and how each lesson is assembled
    licoes.py                   Theory, pitfalls and challenge of each lesson
    teoria_ampliada.py          Reading for each lesson: goal, "How it works", step by step and self-assessment
    exemplos.py                 Example program for 70 lessons
    exemplos_teoricos.py        Example, input and output for the other 21 lessons and the multi-file project
    aprofundamento.py           "Going further", memory diagrams and output of the examples in exemplos.py
    guias_projetos.py           Guides for the 7 projects in module 21
    exercicios.py               Simplified exercises, theory-only lessons and hidden tests
    solucoes.py                 Commented solution of each exercise (unlocked after it passes)
    catalogo_desafios.py        The 100 daily challenges (statement, tests, hints and solution)
    desafios_diarios.py         Daily challenge draw
    referencia.py               Quick reference texts (formats, types, GCC errors, glossary)
    perguntas/                  The 4 theory questions of each lesson (concept, output, error, gap)
  aluno/                        Rules about the student's progress
    situacao.py                 Completed lessons, unlocked modules, next lesson
    gamificacao.py              XP, level, streak, missions and achievements
    teoria.py                   Theory challenge answers and question selection for review and mock exam
    revisao.py                  Spaced repetition
    metas.py                    Daily and weekly goals
    notificacoes.py             Automatic notifications and teacher announcements
    relatorios.py               Profile and mock exam reports and backup file
  compilador/                   Compiler
    executor.py                 Compiles and runs with time, memory and process limits
    terminal.py                 Interactive terminal (WebSocket) and result recording
    correcao.py                 Automatic grading of exercises
    historico.py                History of the latest runs
  rotas/                        Site pages, one area per file
    publico.py                  Home, sign-up, login            -> templates/publico/
    conta.py                    Account settings                -> templates/conta/
    painel.py                   Dashboard, progress, goals, mock exam -> templates/painel/
    estudo.py                   Modules, lesson, exercise       -> templates/estudo/
    desafio_diario.py           Daily challenge                 -> templates/desafio_diario/
    revisao.py                  Review and favorites            -> templates/revisao/
    compilador.py               Free practice and history       -> templates/compilador/
    professor.py                Teacher dashboard and announcements -> templates/professor/
    notificacoes.py             Student notifications           -> templates/notificacoes/
  sessao.py                     Logged-in user in the request
  seguranca.py                  CSRF token and login attempt limit
  usuarios.py                   Account rules: validation, password, deletion, teacher, password links
  preferencias.py               Account preferences (appearance, editor, hints) and accepted values
  envio_email.py                Sending e-mail through the Brevo API
templates/layout/               Base page, menu and editor parts
static/css/style.css            Look of the whole site (dark theme)
static/css/tema-claro.css       Light theme colors
static/js/estudo.js             Theory challenges, lesson completion and search
static/js/terminal.js           Compiler, terminal and automatic draft saving
static/js/editor-c.js           Code editor (CodeMirror)
static/js/layout.js             Menu and terminal windows
static/vendor/                  Third-party libraries (CodeMirror, Socket.IO)
scripts/                        Maintenance scripts (database migration)
tests/                          Automated tests (Python) and browser tests (Playwright)
.github/workflows/testes.yml    Runs the tests and the Docker build on every push to GitHub
```

To change the text of a lesson, edit `backend/conteudo/licoes.py` and `backend/conteudo/teoria_ampliada.py`. The example program lives in `backend/conteudo/exemplos.py` (with its output in `aprofundamento.py`) or in `exemplos_teoricos.py`; the test `tests/test_theory_content.py` compiles every example and checks that the output shown on the page is the real one.

The theory challenge questions live in `backend/conteudo/perguntas/`, four per lesson. The formats are in `base.py`: concept, "what does this program print", "what is wrong with this code" and "what fills the gap". The test `tests/test_perguntas_teoricas.py` compiles and runs the programs with GCC: it checks that the correct option is the real output, that only it fills each gap, and that the code with errors compiles or not, as the question says. It also prevents wrong options from repeating across lessons and the answer's length from giving away the right one.

## Features

- Sign-up with password confirmation, login with "stay signed in" and progress saved in the database
- "Forgot my password" with an e-mail link valid for 1 hour (when e-mail is configured)
- Settings saved to the account, valid on any device: light, dark or system theme, lesson text size, avatar color, reduced animations, code editor (font, indentation, auto-close brackets, line wrapping and shortcut list), hint mode (automatic, on request or off) and confirmation before clearing code
- Account security: change password (signs out other devices), "sign out of all other devices", clear code history, download data and delete the account
- Teacher dashboard: class progress, exercises with the most difficulty, temporary password for students who forgot theirs and announcements to the class
- Teacher access: users listed in `ADMIN_EMAILS` see the whole track completed and unlocked, with commented solutions visible, without counting in class statistics
- Track with 21 modules and 91 lessons, unlocked as the student progresses
- Theory, key points, common mistake and a compilable example in every lesson, with buttons to copy and run the example
- Reading for each lesson: goal, "How it works", step by step and example output, link to the projects and a self-assessment question
- "Going further" in every lesson and memory diagrams in the lessons on arrays, strings, pointers and allocation
- Guides for the projects in module 21, with concepts to review, steps and test cases, and an example multi-file project with a Makefile
- Navigation between lessons, personal notes per lesson and a direct jump to the next lesson on completion
- Quick reference open to everyone: printf/scanf formats, types, operators, functions, translated GCC errors and glossary
- Four theory challenges per lesson (with programs to read, errors to find and gaps to fill) and a code exercise with automatic grading, including hidden tests; at the end of the lesson, a list shows what is still missing to complete it
- Progressive hints: each unsuccessful attempt reveals a new hint specific to the lesson
- Commented solution for all 87 exercises, unlocked only after the grader approves the student's code
- GCC compiler with an interactive terminal (`scanf` really works) in exercises, challenges and free practice; several students can keep programs open at the same time
- 100 original daily challenges (5 per module, with level, example and commented solution), drawn only from those linked to lessons the student has already studied, prioritizing ones not yet done
- XP, levels, leagues, study streak, daily missions and achievements
- Progress tracking with a per-module report, daily and weekly goals and an activity calendar
- Mock exam, spaced repetition, favorites and history of the last 100 runs
- Notifications in the menu (with an unread counter): new daily challenge, unlocked module, today's reviews and teacher announcements; study reminders can be turned off in Settings
- Progress download as JSON
- Screens adapted for phone, tablet and desktop, with light and dark themes
- Protection against cross-site submissions (CSRF), login attempt limit and 8-character passwords

## Running locally

```bash
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Without the `DATABASE_URL` variable, the site creates a SQLite database at `instance/ensinar_c.db` (this file is not pushed to GitHub).

The interactive terminal needs Linux with GCC. On Windows, the pages work, but to compile use Docker:

```bash
docker build -t ensinar-c .
docker run -p 5000:10000 -e SECRET_KEY=change-this ensinar-c
```

## Database (PostgreSQL)

On Render's free tier, files are wiped on every new deploy, so SQLite loses the students' progress. In production the site uses PostgreSQL, set by the `DATABASE_URL` variable.

Render's own free PostgreSQL is deleted 30 days after creation. That is why [Neon](https://neon.tech) is recommended: it is free and does not expire.

1. Create a Neon account and a new project. Pick the region closest to your Render service.
2. Copy the *connection string* (it starts with `postgresql://` and ends with `sslmode=require`).
3. In the Render dashboard, open the service, go to **Environment**, add `DATABASE_URL` with that value and save. Render deploys the site again.
4. On startup, the site creates the tables by itself.

The connection string contains the database password: keep it only in the Render dashboard, never in the code.

To move progress from an old SQLite database to PostgreSQL (the target database must be empty):

```powershell
$env:DATABASE_URL="postgresql://..."
python scripts/migrar_sqlite_para_postgres.py instance/ensinar_c.db
```

## Password recovery e-mail (optional)

Render's free tier blocks e-mail ports (SMTP), so the site sends e-mail through Brevo's HTTPS API, which has a free plan:

1. Create a Brevo account and verify the e-mail that will appear as the sender (under *Senders*).
2. Generate an API key (under *SMTP & API* → *API Keys*).
3. On Render, add `BREVO_API_KEY` with the key and `EMAIL_REMETENTE` with the verified e-mail.

Without these variables, the "Forgot my password" page tells the student to ask the teacher for a temporary password.

## Deploying to Render

The service must be of type **Docker**, because the compiler needs GCC, TCC and WebSocket. The `render.yaml` already points to the `Dockerfile`. With Auto-Deploy on, every `git push` publishes a new version.

## Monitoring

The site has two health-check pages for monitoring services (such as UptimeRobot):

- `/saude` returns `{"site": "ok"}` without querying the database. It can be checked every 5 minutes, since it does not wake Neon up. It is also Render's *Health Check Path*.
- `/saude/banco` runs a `SELECT 1` and returns 503 if the database does not respond. Each query wakes Neon up and uses compute hours from the free plan, so use a long interval, such as 1 hour.

The workflow `.github/workflows/manter-acordado.yml` hits `/saude` every 10 minutes, so Render's free tier does not shut the site down for lack of traffic (which makes the first visit slow). If the site is down, the run fails and GitHub sends an e-mail. GitHub disables scheduled workflows in repositories with no commits for 60 days; in that case, re-enable it under *Actions*.

In practice, GitHub delays scheduled jobs: between October 9 and 13, 2026 this one only ran every 2 to 10 hours, and the site was found asleep (first visit in 32.6 s). To really keep the site awake, use an external service such as [cron-job.org](https://cron-job.org), hitting `https://site-ensinar-c-3.onrender.com/saude` every 10 minutes. The workflow can stay as a backup.

## Tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs these tests with SQLite and PostgreSQL and builds the Docker image on every push.

The tests use a temporary SQLite database and **ignore** `DATABASE_URL`, because they drop the tables. To run them against a disposable PostgreSQL, use `TEST_DATABASE_URL`. The tests that really compile (lesson examples, commented solutions and terminal) are skipped when GCC is not installed.

Browser tests (Playwright), with Chrome or Edge installed:

```bash
npm install --no-save --package-lock=false playwright
npx playwright install webkit
python tests/browser/serve.py
```

In another terminal:

```bash
node tests/browser/responsive.cjs review chrome
node tests/browser/interactions.cjs chrome
node tests/browser/responsive.cjs review webkit
node tests/browser/interactions.cjs webkit
```

Reports and screenshots go to the system temporary folder `ensinar-c-layout`. `LAYOUT_REPORT_DIR` picks another folder and `PLAYWRIGHT_MODULE` uses an existing Playwright installation.

## Environment variables

- `SECRET_KEY`: required in production; `render.yaml` generates one automatically.
- `DATABASE_URL`: PostgreSQL address. Without it, the site uses local SQLite.
- `DB_PATH`: path of the local SQLite database; default is `instance/ensinar_c.db`.
- `DB_POOL_MAX`: maximum open connections to PostgreSQL; default is 5.
- `BREVO_API_KEY` and `EMAIL_REMETENTE`: enable "Forgot my password" by e-mail (see above). `EMAIL_REMETENTE_NOME` changes the sender name; default is Ensinar C.
- `ADMIN_EMAILS`: e-mails (comma-separated) that see the teacher dashboard at `/professor`. Each teacher creates their account through normal sign-up.
- `COMPILER_BACKEND=local`: uses the GCC installed by Docker.
- `MAX_COMPILER_JOBS`: simultaneous compilations; on Render's free tier use `1` (the others wait up to `COMPILER_QUEUE_TIMEOUT` seconds in the queue).
- `MAX_INTERACTIVE_PROGRAMS`: programs open at the same time in the terminal (students waiting on scanf); default is 4. On a paid plan with more memory, 8 or more.
- `COMPILER_INTERACTIVE_MEMORY_MB`: memory for each terminal program; default is 96 MB.
- `COMPILER_MAX_PROCESSES`: maximum processes per compilation or program; default is 8.
- `COMPILER_QUEUE_TIMEOUT`: seconds a compilation waits for its turn; default is 5.
- `COMPILER_RESOURCE_RETRIES`: retries after a temporary process failure; default is 2.
- `COMPILER_COMPILE_TIMEOUT`: maximum compilation time; default is 30 seconds.
- `COMPILER_COMPILE_CPU`: CPU time GCC may use; default is 12 seconds.
- `COMPILER_RUN_TIMEOUT`: limit for runs without interaction (used in hidden tests); default is 8 seconds.
- `COMPILER_INTERACTIVE_TIMEOUT`: time to use the interactive terminal; default is 120 seconds.
- `PISTON_URL` and `PISTON_TOKEN`: optional; used only with `COMPILER_BACKEND=piston`.

## Compiler security

The executor enforces limits on time, memory, processes, files, output and concurrency. In Docker, each program drops privileges and runs as the `compiler-runner` user, with no access to the application files. Even so, a public platform that runs arbitrary code should prefer a separate executor service, isolated by container and network.
