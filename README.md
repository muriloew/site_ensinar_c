# Site Ensinar C

Plataforma web educativa desenvolvida para auxiliar estudantes iniciantes no aprendizado da linguagem C.

## Objetivo

O projeto tem como objetivo organizar o ensino da linguagem C em módulos progressivos, com teoria curta, exemplos de código, desafios práticos e acompanhamento de progresso.

## Tecnologias utilizadas

- HTML
- CSS
- JavaScript
- Python
- Flask
- GitHub
- Render

## Funcionalidades

- Página inicial explicando a proposta do projeto
- Módulos progressivos de aprendizagem
- Lições com teoria, exemplos e explicação
- Desafios automáticos com verificação de resposta
- Barra de progresso
- Salvamento de progresso no navegador com localStorage
- Área de escrita de código em C

## Estrutura

```txt
site_ensinar_c/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── modulos.html
│   ├── modulo.html
│   └── erro.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── progresso.js
│       └── desafios.js
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```

## Como executar localmente

```bash
pip install -r requirements.txt
python app.py
```

Depois acesse:

```txt
http://127.0.0.1:5000
```

## Publicação

O projeto pode ser publicado no Render utilizando o arquivo `render.yaml`.

## Observação

O compilador integrado real ainda pode ser implementado em uma versão futura. Na versão atual, existe uma área de escrita de código para apoiar os estudos.
