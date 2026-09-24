# Histórico de versões do Ensinar C

Registro das mudanças feitas em cada versão do site, da mais antiga para a mais nova.

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


## Versão 23 — Desafios por lição e progresso diário

- Cada lição agora possui três desafios teóricos dentro da própria página de conteúdo.
- Cada resposta é salva separadamente e a lição só é liberada quando todas estão corretas.
- As alternativas aparecem em posições variadas, sem deixar a resposta correta sempre em primeiro lugar.
- Progresso de versões antigas continua reconhecido.
- O módulo 1 permanece sem exercícios de código e apresenta apenas a base conceitual.
- Os desafios diários ficam bloqueados enquanto o aluno está no módulo 1.
- Há 10 desafios diários para cada módulo do 2 ao 21, totalizando 200 atividades.
- O sorteio diário usa somente módulos liberados pelo progresso do aluno.
- O backend também bloqueia tentativas de acessar lições ou desafios avançados diretamente.
- A lógica de desafios diários e respostas teóricas foi separada na pasta `backend`.


## Versão 24 — Jornada gamificada

- O painel agora destaca a próxima missão e as fases próximas do aluno.
- Foram adicionadas três missões renovadas diariamente, com progresso e recompensa de XP resgatável uma única vez.
- A sequência de estudos passou a usar dias reais, guardar o recorde e oferecer proteção para uma ausência.
- A página de módulos foi transformada em uma jornada de 21 fases com bloqueios, estrelas e busca.
- O perfil agora reúne calendário de atividade, nível, liga e coleção de conquistas por raridade.
- As conquistas foram ampliadas para lições, módulos, desafios, simulados, XP e sequência.
- O backup automático inclui o histórico de atividades e as recompensas diárias.
- Respostas teóricas já acertadas não podem ser repetidas para aumentar artificialmente o progresso das missões.


## Versão 25 — Segurança, revisão e histórico

- O compilador foi separado em `backend/compilador.py` e recebeu limites de CPU, memória, processos, arquivos, saída, tempo e concorrência.
- O processo interativo agora registra corretamente sucesso, falha e cancelamento, sem aprovar uma execução com erro.
- Alterar um rascunho invalida a aprovação anterior; nada é compilado antes do clique do aluno.
- A correção automática usa casos ocultos adicionais em atividades com entrada e decisões.
- Foram adicionados favoritos, revisão espaçada e histórico completo de códigos.
- O perfil mostra estatísticas de teoria, exercícios e compilações por módulo.
- O backup passou a incluir histórico de códigos, favoritos e revisões, com gravação atômica e retenção das 20 cópias mais recentes.
- Cookies e WebSocket foram restringidos para produção, e o Docker não inclui banco nem backups locais na imagem.


## Versão 26 — Editor C e correção de timeout

- O tempo de compilação passou de 8 para 30 segundos para funcionar em instâncias gratuitas com CPU reduzida.
- O limite de CPU permanece separado do tempo de parede, preservando a interrupção de compilações abusivas.
- O Gunicorn agora permite até 75 segundos para a requisição completa de compilação e execução.
- Cliques repetidos em Compilar são bloqueados enquanto o build atual estiver em andamento.
- O Build log mostra a duração real da compilação.
- Os editores usam CodeMirror armazenado localmente, com sintaxe C, linhas, pares e chaves automáticos, indentação e busca.
- Foram adicionados autocompletar C, desfazer/refazer, formatação, comentário rápido, movimentação e duplicação de linhas.
- `Ctrl+Enter` compila, `Ctrl+S` salva, `Ctrl+Espaço` sugere comandos e `Ctrl+/` comenta a linha.
- A prática livre preserva o rascunho no navegador e continua sem executar nada automaticamente.


## Versão 27 — Compilador estável no Render gratuito

- O Render executa somente uma compilação por vez e mantém as demais em uma fila curta.
- O GCC continua principal; o TCC assume automaticamente somente em falhas de infraestrutura como `vfork: Resource temporarily unavailable`.
- No runtime Python compartilhado, `nproc` não é aplicado porque ele também contaria as threads do Gunicorn; no Docker, o usuário isolado mantém o limite rígido.
- Programas e subprocessos remanescentes são encerrados mesmo quando o processo principal já terminou.
- O `Procfile` usa 2 threads, o Docker usa 4, e ambos permitem uma compilação por vez com duas tentativas para falhas temporárias.
- O build log identifica quando o compilador alternativo foi utilizado.


## Revisão de telas e compatibilidade — setembro de 2026

- Colunas e textos ajustam-se a celulares, tablets, notebooks e monitores, inclusive com zoom do navegador.
- O menu lateral tem rolagem em telas baixas. Em telas menores, o menu horizontal destaca a pagina atual.
- O terminal ajusta sua altura ao espaco visivel, incluindo a abertura do teclado do celular; a entrada e os botoes permanecem acessiveis.
- O editor atualiza suas medidas ao redimensionar a janela e continua funcionando quando o navegador bloqueia armazenamento local.
- Fechar ou limpar uma execucao libera novamente o botao Compilar.
- CSS e JavaScript recebem uma versao na URL para renovar o cache quando os arquivos mudam.
- O cliente Socket.IO 4.7.5 e servido pelo proprio site, mantendo a mesma versao e os mesmos eventos do terminal.


## Versão 28 — Reorganização, PostgreSQL e limpeza

- O `app.py` de 4 mil linhas foi dividido em `backend/` (banco, conteúdo, aluno, compilador e rotas); templates e scripts ficam em pastas com o mesmo nome da área.
- O site passa a usar PostgreSQL quando a variável `DATABASE_URL` está definida; sem ela continua usando SQLite local.
- O backup automático em arquivos foi removido: o progresso fica no banco e o botão **Baixar backup** gera a cópia na hora.
- Script `scripts/migrar_sqlite_para_postgres.py` copia um banco SQLite antigo para o PostgreSQL.
- Removidos: trilha antiga sobrescrita, versões 14 a 17 do terminal em JavaScript, rotas HTTP de compilação sem uso, páginas sem rota, `Procfile`, `runtime.txt` e 44 regras de CSS sem uso.
- O banco pessoal (`instance/ensinar_c.db`) e o zip antigo deixaram de ser enviados ao GitHub.
- Correções: pontos-chave das lições iniciais, casos ocultos do `scanf`, dica após 3 tentativas, Ctrl+S apagando a aprovação, metas contando lições editadas, redirecionamento dos favoritos, mensagem de conclusão sem login.
- O build log mostra `programa.c:linha:coluna` e o terminal explica falha de segmentação, divisão por zero e limites de tempo.
- Cada página lê o progresso do aluno uma única vez, em vez de uma consulta por módulo.
- Token CSRF em todos os envios, bloqueio de 15 minutos após 5 senhas erradas e senha mínima de 8 caracteres.
- Dicas progressivas específicas de cada lição e desafio diário, liberadas a cada tentativa sem sucesso.
- Tema claro com botão no menu; segue a preferência do sistema até o aluno escolher.
- GitHub Actions roda os testes com SQLite e PostgreSQL e monta a imagem Docker a cada push.


## Versão 29 — Conta, professor, lições e consulta rápida

- Cadastro com confirmação de senha, validação de e-mail e opção "mostrar senha"; login com "continuar conectado" por 30 dias.
- Página **Configurações**: editar nome e e-mail (trocar o e-mail pede a senha), trocar senha, tema, tamanho da letra do editor, baixar os dados e excluir a conta com todo o progresso.
- **Painel do professor** (`/professor`, liberado pela variável `ADMIN_EMAILS`): resumo da turma, tabela de alunos, exercícios com mais tentativas sem sucesso e senha temporária para alunos que esqueceram a senha, com troca obrigatória no primeiro acesso.
- Lições: posição no módulo, lição anterior e próxima, ir direto para a próxima ao concluir, copiar o exemplo, executar o exemplo no compilador, anotações pessoais e botão "Restaurar código inicial" nos exercícios e desafios.
- **Consulta rápida** (`/referencia`), aberta também a visitantes, com busca: formatos do printf/scanf, tipos e tamanhos, operadores por prioridade, sequências de escape, funções mais usadas, mensagens do GCC traduzidas e glossário.
- Acentos corrigidos nas perguntas dos desafios teóricos e nas mensagens do compilador (as respostas corretas não mudaram).
- Ícone do site, descrição para buscadores e cabeçalhos de segurança (nosniff, proteção contra exibição em frames de outros sites).


## Versão 30 — Turma, senha por e-mail, soluções e aprofundamento

- Compilador para a turma: compilar entra em uma fila curta e o programa aberto no terminal ocupa uma vaga separada (4 por padrão, `MAX_INTERACTIVE_PROGRAMS`). Um aluno parado no `scanf` não bloqueia mais os outros; quando as vagas acabam, a mensagem pede para fechar o terminal ou aguardar.
- **Esqueci minha senha**: link por e-mail válido por 1 hora e de uso único, enviado pela API do Brevo (`BREVO_API_KEY` e `EMAIL_REMETENTE`). No banco fica só o hash do link. Sem o e-mail configurado, a página orienta a pedir uma senha temporária ao professor.
- **Solução comentada** para os 87 exercícios de código e para os desafios diários. Ela só aparece depois que a correção automática aprova o código do aluno (ou a lição já foi concluída) e se abre na hora, sem recarregar a página. Todas as soluções compilam sem avisos e passam na própria correção automática (teste `tests/test_solucoes.py`).
- **Leituras das lições** (enviadas ao `main` em paralelo e integradas à nova organização): objetivo, "Como funciona", passo a passo e saída do exemplo, ligação com os projetos, pergunta de autoavaliação, 21 exemplos mais completos, projeto em vários arquivos com Makefile e roteiro dos 7 projetos do módulo 21. Os arquivos ficam em `backend/conteudo/` (`teoria_ampliada.py`, `exemplos_teoricos.py` e `guias_projetos.py`).
- **Indo além** nas 91 lições, com detalhes, armadilhas e ferramentas, e tabela "Como fica a memória" nas lições de arrays, strings, ponteiros, alocação, unions e listas.
- Exemplos novos onde várias lições repetiam o mesmo programa: else, do while, criando função, parâmetros, retorno, memória, structs, typedef e .h, cada um com passo a passo próprio.
- O teste `tests/test_theory_content.py` compila os 91 exemplos com `-Werror` e confere se a saída mostrada na página é a real.
