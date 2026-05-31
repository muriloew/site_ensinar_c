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
