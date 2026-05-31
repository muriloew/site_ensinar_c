# Site Ensinar C

Plataforma web educativa criada como parte prática de um Trabalho de Conclusão.

## Objetivo

O projeto tem como objetivo auxiliar estudantes iniciantes no aprendizado da linguagem de programação C, utilizando módulos progressivos, exemplos de código, desafios automáticos e acompanhamento de progresso.

## Tecnologias utilizadas

- HTML
- CSS
- JavaScript
- Python
- Flask
- GitHub
- Render

## Funcionalidades implementadas

- Página inicial explicando a proposta do projeto
- Página de módulos
- Página individual para cada módulo
- Lições com teoria curta
- Exemplos de código em C
- Explicação dos códigos
- Desafios com verificação automática
- Barra de progresso
- Salvamento do progresso no navegador com localStorage
- Área de escrita de código
- Página sobre o projeto
- Configuração para publicação no Render

## Estrutura do projeto

```txt
site_ensinar_c/
├── app.py
├── backend/
│   └── __init__.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── modulos.html
│   ├── modulo.html
│   ├── sobre.html
│   └── erro.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── progresso.js
│   │   └── desafios.js
│   └── img/
├── requirements.txt
├── Procfile
├── render.yaml
├── .gitignore
└── README.md
```

## Como rodar localmente

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o projeto:

```bash
python app.py
```

Depois acesse no navegador:

```txt
http://127.0.0.1:5000
```

## Como enviar para o GitHub

```bash
git add .
git commit -m "Atualiza parte pratica do site"
git push
```

## Observação sobre o compilador integrado

Nesta versão, foi criada uma área de escrita de código. O compilador real de C fica como melhoria futura, podendo ser implementado com uma API segura ou serviço externo de execução de código.
