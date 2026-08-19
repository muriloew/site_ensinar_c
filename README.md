# Ensinar C - versão corrigida

Plataforma web educativa para ensino da linguagem C.

## Recursos

- Cadastro com e-mail único
- Login com conta salva
- Progresso salvo em SQLite
- XP, nível, ranking e conquistas
- Módulos bloqueados e desbloqueados
- Desafio diário com código
- Exercício de código no final de cada lição
- Editor de código nas lições
- Rota para compilar e executar código C usando GCC quando disponível
- Terminal interativo real nos exercícios e desafios diários
- Correção automática de exercícios e desafios antes da conclusão
- Rodízio com maior variedade de desafios diários
- Trilha ampliada para 21 módulos e 91 lições, cobrindo introdução, variáveis, operadores, decisão, repetição, funções, arrays, strings, ponteiros, memória, structs, arquivos, modularização, bibliotecas, bits, debug, GCC, segurança, estruturas de dados, algoritmos e projetos
- Conteúdo teórico próprio em cada lição, com fundamento, pontos-chave, erro comum e exemplo compilável
- Desafios práticos específicos para todas as 91 lições, com critérios e saídas esperadas
- Backup automático do progresso em `instance/backups`
- Perfil do usuário com relatório de desempenho
- Metas diárias e semanais configuráveis
- Simulado de prova com correção automática e histórico
- Busca por módulos e conteúdos
- Navegação e telas ajustadas para uso em celulares
- Modo prática livre exposto no menu
- Sem certificado, pois o projeto não possui licença para certificação oficial

## Como rodar localmente

```bash
python -m pip install -r requirements.txt
python app.py
```

Acesse:

```txt
http://127.0.0.1:5000
```

## Render

Build Command:

```txt
pip install -r requirements.txt
```

Start Command:

```txt
gunicorn app:app
```

## Observação importante

O compilador usa `gcc` no servidor. Se o ambiente não tiver GCC instalado, o site mostrará uma mensagem explicando que o compilador não está disponível. Para produção, o ideal é usar uma API externa segura de compilação ou configurar um ambiente isolado.


## Alterações da versão 4

- Teoria e exercício de código foram separados em páginas diferentes.
- O exercício de código agora abre com código mínimo, para o usuário completar.
- O desafio teórico usa JavaScript com `data-resposta`, evitando erro ao clicar em alternativas.
- Lições já concluídas continuam acessíveis.
- O código salvo pelo usuário permanece ao voltar no exercício.


## Correções da versão 5

- Adicionada migração automática do banco SQLite para corrigir usuários/progresso antigos.
- Corrigido erro 500 ao abrir módulo já concluído em versões antigas.
- Corrigido salvamento do desafio teórico.
- Melhorado retorno de erro do compilador.
- Se o servidor não tiver GCC, o código é salvo e a tela explica o motivo da não execução.


## Versão 6

- Adicionada entrada do terminal para programas com scanf.
- A entrada digitada é enviada para o programa durante a execução.
- Adicionado painel de passo a passo do código, explicando linha por linha.
- Entrada do terminal e código do usuário ficam salvos.


## Versão 7

- Removido o passo a passo no final.
- Adicionada interface semelhante ao Code::Blocks:
  - botão Compilar;
  - botão Executar;
  - Build log;
  - Terminal de entrada;
  - Terminal de saída.
- A entrada do terminal é enviada para programas com scanf.


## Versão 8

- Build log, entrada do terminal e saída foram movidos para uma janela integrada separada.
- A janela funciona como console do ambiente, com abas:
  - Entrada;
  - Build log;
  - Saída.
- Os botões Compilar e Executar abrem automaticamente a aba correta.


## Versão 9

- A resposta do desafio teórico é salva ao responder, mesmo sem concluir a lição.
- O console agora fica em uma única janela integrada.
- Removida a separação em abas.
- O botão Compilar agora compila e executa.
- A janela tem apenas Compilar e Sair.
- A saída mostra entrada do usuário, saída do programa e build log juntos.


## Versão 10

- A resposta do desafio teórico agora permanece visualmente marcada ao trocar de tela.
- Também há fallback em localStorage para manter a marcação na interface.
- O console foi redesenhado para ficar parecido com a janela do Code::Blocks.
- A saída mostra o prompt com a entrada digitada na mesma linha, quando possível.


## Versão 11

- Adicionado Compilador Online separado em `/compilador`.
- O compilador usa API externa Piston quando disponível.
- Mantém fallback com GCC local.
- Adicionado histórico recente de códigos executados.
- Lições agora podem abrir o compilador completo com o código inicial do exercício.


## Versão 12

- Corrigida rota `/compilador?licao_id=...`.
- Removido compilador rápido da página de exercício.
- Agora existe apenas o compilador completo separado.
- Página de exercício só direciona para o compilador completo.


## Versão 13

- O compilador aparece apenas no exercício de código de cada módulo.
- Removido link do compilador no menu lateral.
- O usuário escreve código em uma tela parecida com editor.
- Ao clicar Compilar:
  - abre uma janela para entrada do scanf;
  - se houver erro, abre Build Log;
  - se compilar, abre terminal estilo Code::Blocks.


## Versão 14

- Removido popup separado de entrada.
- Ao clicar Compilar, abre diretamente a janela estilo Code::Blocks.
- A entrada é digitada dentro da própria janela do terminal.
- O botão Compilar dentro do terminal executa o programa com a entrada digitada.


## Versão 15

- Terminal no estilo Code::Blocks:
  - compila primeiro;
  - se não tiver erro, abre o terminal;
  - mostra o prompt do programa;
  - o usuário digita a entrada dentro da janela;
  - depois o terminal mostra a saída completa.


## Versão 16

- Removida chamada para `/api/exercicio/preparar-terminal`, evitando erro 500 antes da execução.
- O prompt do scanf é detectado no navegador.
- Removidas dicas amarelas fixas.
- Dica aparece apenas após algumas tentativas de compilação com erro.


## Versão 17

- Terminal simulado no estilo Code::Blocks:
  - mostra o prompt primeiro;
  - usuário digita dentro da janela;
  - Enter ou Enviar executa o programa;
  - saída final é formatada como Code::Blocks.


## Versão 18 — Compilador real

Esta versão implementa um compilador interativo real usando:

- GCC;
- Flask-SocketIO;
- WebSocket;
- pseudo-terminal Linux (`pty`);
- stdin/stdout em tempo real.

### Importante

Para funcionar no Render, use deploy por Docker, pois o ambiente precisa instalar GCC.

No Render:
- Runtime: Docker
- Dockerfile: `./Dockerfile`

O terminal agora funciona de forma real:
- `printf` aparece;
- `scanf` espera entrada;
- usuário digita no terminal;
- programa continua depois da entrada.


## Versão 19 — Correção Render

O erro `eventlet.green.thread has no attribute start_joinable_thread` acontece quando o Render roda o projeto como serviço Python usando Python 3.14.

Esta versão deve ser publicada como **Docker Web Service**, porque:
- precisa de Python 3.11;
- precisa de GCC;
- precisa de WebSocket com eventlet;
- precisa de terminal real com stdin/stdout.

### Como publicar no Render

Crie um novo serviço:

1. New
2. Web Service
3. Conecte o repositório
4. Runtime: Docker
5. Dockerfile Path: `./Dockerfile`

Não use o serviço Python antigo para esta versão.

Se usar o serviço antigo, ele continuará tentando rodar:
`gunicorn app:app`
ou Python 3.14, e vai falhar.

### Comando usado no Docker

```txt
gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:$PORT
```


## Versão 20 — Compilador real corrigido

Esta versão remove o `eventlet`, porque ele quebrou no Render com Python 3.14.

Agora usa:
- Flask-SocketIO;
- `async_mode="threading"`;
- `simple-websocket`;
- Gunicorn com threads;
- Docker com Python 3.11;
- GCC instalado no container.

### Deploy correto no Render

Use **novo Web Service com Runtime Docker**.

Configuração:
- Runtime: Docker
- Dockerfile Path: `./Dockerfile`

Não use o serviço Python antigo, porque ele roda Python 3.14 e não instala GCC.

### Comando usado no Docker

```txt
gunicorn -w 1 --threads 8 app:app --bind 0.0.0.0:$PORT
```

### Como testar local

Instale GCC no computador e rode:

```bash
python -m pip install -r requirements.txt
python app.py
```


## Versão 21 — Conteúdo e exercícios revisados

- As 91 lições agora possuem teoria específica, pontos-chave e alertas de erros comuns.
- Cada lição recebeu um desafio prático alinhado ao assunto estudado.
- A correção automática verifica recursos obrigatórios, saída e entradas de teste quando necessário.
- Os códigos iniciais são estruturas C11 válidas para o aluno completar.
- Todos os caminhos locais de compilação usam as mesmas opções do GCC:
  - `-std=c11`
  - `-Wall`
  - `-Wextra`
  - `-pedantic`
  - `-lm`
- Códigos vazios ou maiores que 100 KB são rejeitados antes da compilação.


## Versão 22 — Perfil, metas, simulado e mobile

- Adicionada página de perfil com progresso geral, relatório por módulo e atividades recentes.
- Adicionadas metas diárias e semanais para lições e desafios.
- Adicionado simulador de prova com questões dos módulos liberados, correção automática e histórico.
- Adicionada busca por módulos e conteúdos na página de módulos.
- O modo prática livre foi colocado no menu lateral usando o compilador existente.
- Melhorada a navegação em telas pequenas, com menu horizontal e ajustes no editor/terminal.
- O backup automático agora inclui metas e resultados de simulados.
