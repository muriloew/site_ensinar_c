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
