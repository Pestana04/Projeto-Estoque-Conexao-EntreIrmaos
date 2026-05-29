# EntreIrmaos — Sistema de Controle de Estoque para Doações 📦

Sistema web desenvolvido para auxiliar a instituição **EntreIrmaos** no gerenciamento de doações, controle de estoque e organização de itens recebidos e distribuídos pela instituição.

O projeto tem como objetivo fornecer uma plataforma simples, intuitiva e segura para registrar entradas e saídas de produtos, além de apresentar um painel visual de acompanhamento do estoque em tempo real.

---

# Objetivo do Projeto

O sistema foi desenvolvido como parte de um projeto acadêmico, buscando aplicar conceitos de:

* Desenvolvimento Web com Python
* Manipulação de arquivos Excel
* Controle de concorrência
* Organização de estoque
* Estruturação de dashboards
* Boas práticas de desenvolvimento colaborativo com Git/GitHub

Além do ambiente acadêmico, o projeto também possui potencial de utilização real pela instituição.

---

# Funcionalidades Implementadas

## 📊 Painel Geral (Dashboard)

O sistema possui um dashboard visual com:

* Quantidade total de itens em estoque
* Quantidade de itens armazenados no instituto
* Quantidade de itens enviados ao bazar
* Visualização organizada dos produtos cadastrados

---

## 📥 Entrada de Doações

Tela responsável pelo registro de novas doações recebidas.

Permite cadastrar:

* Nome do produto
* Categoria
* Quantidade
* Local de armazenamento

---

## 📤 Baixa de Estoque

Responsável pela saída de itens do estoque.

O sistema registra:

* Nome do responsável pela retirada
* Telefone de contato
* Produto retirado
* Quantidade removida

---

## 🔒 Controle de Concorrência (File Lock)

Como o sistema utiliza arquivos Excel para armazenamento de dados, foi necessário implementar um mecanismo de controle de concorrência para evitar:

* Escritas simultâneas no arquivo
* Corrupção de dados
* Perda de informações
* Race conditions

Para isso, foi utilizado o conceito de **File Lock**, garantindo que apenas uma operação possa modificar o arquivo por vez.

Esse mecanismo é essencial para manter a integridade dos dados em ambientes com múltiplos acessos simultâneos.

---

# Tecnologias Utilizadas

## Backend

* Python
* Flask

## Manipulação de Dados

* Pandas
* OpenPyXL

## Controle de Concorrência

* FileLock

## Frontend

* HTML5
* CSS3
* JavaScript

## Versionamento

* Git
* GitHub

---

# Estrutura Inicial do Projeto

```bash
Projeto-Estoque-Conexao-EntreIrmaos/
│
├── app.py
├── requirements.txt
├── estoque.xlsx
│
├── services/
│   ├── lock_excel.py
│   └── estoque_service.py
│
├── templates/
│   ├── dashboard.html
│   ├── entrada.html
│   └── baixa.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
└── README.md
```

---

# Como Executar o Projeto

## 1. Clone o repositório

```bash
git clone https://github.com/Pestana04/Projeto-Estoque-Conexao-EntreIrmaos.git
```

---

## 2. Acesse a pasta do projeto

```bash
cd Projeto-Estoque-Conexao-EntreIrmaos
```

---

## 3. Crie um ambiente virtual

### Windows

```bash
python -m venv .venv
```

Ative:

```bash
.venv\Scripts\activate
```

---

## 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 5. Execute o sistema

```bash
python app.py
```

---

## 6. Acesse no navegador

```text
http://localhost:5000
```

---

# Decisões de Desenvolvimento

## Uso de Excel como armazenamento

Optou-se inicialmente pela utilização de arquivos Excel devido à simplicidade de implementação e facilidade de utilização pela instituição.

Isso permite:

* Fácil visualização dos dados
* Compatibilidade com ferramentas administrativas
* Facilidade de exportação e backup

---

## Implementação de File Lock

Como múltiplos usuários podem acessar o sistema simultaneamente, foi necessário implementar um mecanismo de bloqueio de arquivo para evitar inconsistências.

O sistema utiliza um arquivo `.lock` temporário durante operações de leitura e escrita.

---

## Interface Visual

A interface foi desenvolvida com foco em:

* Simplicidade
* Facilidade de uso
* Organização visual
* Acessibilidade para usuários não técnicos

---

# Possíveis Melhorias Futuras

* Hospedagem online do sistema
* Migração para banco de dados
* Sistema de login e permissões
* Histórico completo de movimentações
* Relatórios automáticos
* Integração com QR Code
* Dashboard analítico avançado
* Controle de validade de produtos
* Sistema de notificações

---

# Considerações Finais

O projeto busca unir tecnologia e impacto social, auxiliando a instituição EntreIrmaos na organização e controle das doações recebidas..

Além do aprendizado acadêmico, o sistema foi pensado para possuir aplicabilidade real, contribuindo diretamente para a eficiência operacional da instituição.
