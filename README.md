# Ensinar C

Plataforma web para aprender a linguagem C: 21 módulos e 91 lições com teoria, desafios teóricos, exercícios corrigidos automaticamente e um compilador GCC com terminal interativo no navegador.

O histórico de mudanças de cada versão está em [`docs/historico-versoes.md`](docs/historico-versoes.md).

## Onde fica cada coisa

```txt
app.py                          Ponto de entrada: monta o site (o Gunicorn usa app:app)
backend/
  banco/
    conexao.py                  Conexão: PostgreSQL com DATABASE_URL, senão SQLite local
    tabelas.py                  Criação das tabelas e atualização de bancos antigos
  conteudo/                     O que o aluno estuda
    trilha.py                   Os 21 módulos e a montagem de cada lição
    licoes.py                   Teoria, cuidados e desafio de cada lição
    exemplos.py                 Programa de exemplo de cada lição
    exercicios.py               Exercícios simplificados, lições só teóricas e testes ocultos
    desafios_diarios.py         Geração e sorteio dos desafios diários
  aluno/                        Regras sobre o progresso do aluno
    situacao.py                 Lições concluídas, módulos liberados, próxima lição
    gamificacao.py              XP, nível, sequência, missões e conquistas
    teoria.py                   Respostas dos desafios teóricos
    revisao.py                  Revisão espaçada
    metas.py                    Metas diárias e semanais
    relatorios.py               Relatórios do perfil, simulado e arquivo de backup
  compilador/
    executor.py                 Compila e executa com limites de tempo, memória e processos
    terminal.py                 Terminal interativo (WebSocket) e gravação dos resultados
    correcao.py                 Correção automática dos exercícios
    historico.py                Histórico das últimas execuções
  rotas/                        Páginas do site, uma área por arquivo
    publico.py                  Início, cadastro, login        -> templates/publico/
    painel.py                   Painel, perfil, metas, simulado -> templates/painel/
    estudo.py                   Módulos, lição, exercício       -> templates/estudo/
    desafio_diario.py           Desafio diário                  -> templates/desafio_diario/
    revisao.py                  Revisão e favoritos             -> templates/revisao/
    compilador.py               Prática livre e histórico       -> templates/compilador/
  sessao.py                     Usuário logado na requisição
templates/layout/               Página base, menu e partes do editor
static/css/style.css            Visual de todo o site
static/js/estudo.js             Desafios teóricos, conclusão de lições e busca
static/js/terminal.js           Compilador, terminal e rascunho automático
static/js/editor-c.js           Editor de código (CodeMirror)
static/js/layout.js             Menu e janelas do terminal
static/vendor/                  Bibliotecas de terceiros (CodeMirror, Socket.IO)
scripts/                        Scripts de manutenção (migração do banco)
tests/                          Testes automáticos (Python) e de navegador (Playwright)
```

Para mudar o texto de uma lição, edite `backend/conteudo/licoes.py`; para mudar o programa de exemplo, `backend/conteudo/exemplos.py`.

## Recursos

- Cadastro com e-mail único, login e progresso salvo no banco de dados
- Trilha com 21 módulos e 91 lições, liberados conforme o avanço
- Teoria, pontos-chave, erro comum e exemplo compilável em cada lição
- Três desafios teóricos por lição e exercício de código com correção automática, incluindo testes ocultos
- Compilador GCC com terminal interativo (`scanf` funciona de verdade) nos exercícios, desafios e prática livre
- 200 desafios diários, sorteados só entre os módulos já liberados
- XP, níveis, ligas, sequência de estudos, missões diárias e conquistas
- Perfil com relatório por módulo, metas diárias e semanais e calendário de atividade
- Simulado, revisão espaçada, favoritos e histórico das 100 últimas execuções
- Download do progresso em JSON
- Telas ajustadas para celular, tablet e computador

## Como rodar no computador

```bash
python -m pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`. Sem a variável `DATABASE_URL`, o site cria um SQLite em `instance/ensinar_c.db` (esse arquivo não vai para o GitHub).

O terminal interativo precisa de Linux com GCC. No Windows, as páginas funcionam, mas para compilar use o Docker:

```bash
docker build -t ensinar-c .
docker run -p 5000:10000 -e SECRET_KEY=troque-isto ensinar-c
```

## Banco de dados (PostgreSQL)

No Render gratuito os arquivos são apagados a cada nova publicação, então o SQLite perde o progresso dos alunos. Em produção o site usa PostgreSQL, indicado pela variável `DATABASE_URL`.

O PostgreSQL gratuito do próprio Render é apagado 30 dias depois de criado. Por isso a recomendação é o [Neon](https://neon.tech), que é gratuito e não expira:

1. Crie uma conta no Neon e um projeto novo. Escolha a região mais próxima do seu serviço no Render.
2. Copie a *connection string* (começa com `postgresql://` e termina com `sslmode=require`).
3. No painel do Render, abra o serviço, vá em **Environment**, adicione `DATABASE_URL` com esse valor e salve. O Render publica o site de novo.
4. Ao iniciar, o site cria as tabelas sozinho.

A connection string contém a senha do banco: guarde-a só no painel do Render, nunca no código.

Para levar o progresso de um SQLite antigo para o PostgreSQL (o banco de destino precisa estar vazio):

```powershell
$env:DATABASE_URL="postgresql://..."
python scripts/migrar_sqlite_para_postgres.py instance/ensinar_c.db
```

## Publicar no Render

O serviço deve ser do tipo **Docker**, pois o compilador precisa de GCC, TCC e WebSocket. O `render.yaml` já aponta para o `Dockerfile`. Com o Auto-Deploy ativo, cada `git push` publica uma nova versão.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes usam um SQLite temporário e **ignoram** a `DATABASE_URL`, porque apagam as tabelas. Para testá-los em um PostgreSQL descartável, use `TEST_DATABASE_URL`. O teste de compilação real é ignorado quando o GCC não está instalado.

Testes de navegador (Playwright), com Chrome ou Edge instalado:

```bash
npm install --no-save --package-lock=false playwright
npx playwright install webkit
python tests/browser/serve.py
```

Em outro terminal:

```bash
node tests/browser/responsive.cjs review chrome
node tests/browser/interactions.cjs chrome
node tests/browser/responsive.cjs review webkit
node tests/browser/interactions.cjs webkit
```

Os relatórios e capturas ficam na pasta temporária `ensinar-c-layout` do sistema. `LAYOUT_REPORT_DIR` escolhe outra pasta e `PLAYWRIGHT_MODULE` usa uma instalação existente do Playwright.

## Variáveis de ambiente

- `SECRET_KEY`: obrigatória em produção; o `render.yaml` gera uma automaticamente.
- `DATABASE_URL`: endereço do PostgreSQL. Sem ela, o site usa SQLite local.
- `DB_PATH`: caminho do SQLite local; o padrão é `instance/ensinar_c.db`.
- `DB_POOL_MAX`: máximo de conexões abertas com o PostgreSQL; o padrão é 5.
- `COMPILER_BACKEND=local`: usa o GCC instalado pelo Docker.
- `MAX_COMPILER_JOBS`: compilações simultâneas; no Render gratuito use `1`.
- `COMPILER_MAX_PROCESSES`: máximo de processos por compilação ou programa; o padrão é 8.
- `COMPILER_QUEUE_TIMEOUT`: segundos que uma compilação aguarda sua vez; o padrão é 5.
- `COMPILER_RESOURCE_RETRIES`: tentativas após uma falha temporária de processos; o padrão é 2.
- `COMPILER_COMPILE_TIMEOUT`: tempo máximo da compilação; o padrão é 30 segundos.
- `COMPILER_COMPILE_CPU`: CPU que o GCC pode consumir; o padrão é 12 segundos.
- `COMPILER_RUN_TIMEOUT`: limite de execução sem interação (usado nos testes ocultos); o padrão é 8 segundos.
- `COMPILER_INTERACTIVE_TIMEOUT`: tempo para usar o terminal interativo; o padrão é 120 segundos.
- `PISTON_URL` e `PISTON_TOKEN`: opcionais; usados somente com `COMPILER_BACKEND=piston`.

## Segurança do compilador

O executor aplica limites de tempo, memória, processos, arquivos, saída e concorrência. No Docker, cada programa perde privilégios e roda com o usuário `compiler-runner`, sem acesso aos arquivos da aplicação. Ainda assim, uma plataforma pública que execute código arbitrário deve preferir um serviço executor separado, com isolamento por container e rede.
