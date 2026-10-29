# 🐧 Automação Linux

[![Linux Automation Lab CI](https://github.com/RegisFredFilho/automacao-ansible/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/RegisFredFilho/automacao-ansible/actions/workflows/ci.yml)

Laboratório prático de **automação de infraestrutura Linux com Ansible**, utilizando Python para testes automatizados, Nginx como serviço web, GitHub Actions para integração contínua e Cloudflare Access para proteger o acesso externo.

O projeto foi desenvolvido em um ambiente de homelab com Proxmox VE, com foco em administração Linux, Infrastructure as Code (IaC), automação, testes e boas práticas de DevOps.

## 🎯 Objetivos

- Provisionar e configurar servidores Debian remotamente por SSH.
- Automatizar a instalação e configuração do Nginx.
- Organizar automações em roles reutilizáveis.
- Utilizar templates Jinja2 e handlers.
- Demonstrar idempotência nas execuções do Ansible.
- Validar serviços com testes Python e pytest.
- Implementar integração contínua com GitHub Actions.
- Monitorar um endpoint HTTPS protegido pelo Cloudflare Access.

## 🏗️ Arquitetura

```text
              GitHub Repository
                      |
               GitHub Actions
                 /         \
          Unit Tests    HTTP Integration
                            |
                     Cloudflare Access
                            |
                     Cloudflare Tunnel
                            |
                    Nginx (ansible-node)
                            ^
                            |
                       SSH + Ansible
                            |
                    ansible-controller
                            |
                        Proxmox VE
```

O ambiente utiliza duas máquinas virtuais Debian:

| Máquina | Responsabilidade |
|---|---|
| ansible-controller | Executa playbooks Ansible e testes Python |
| ansible-node | Recebe a configuração automatizada e hospeda o Nginx |

O controlador se comunica com o nó por SSH. O GitHub Actions realiza os testes de código e, mediante execução manual, verifica o serviço HTTPS com autenticação por Service Token.

## 🛠️ Tecnologias

| Tecnologia | Utilização |
|---|---|
| Proxmox VE | Virtualização do laboratório |
| Debian Linux | Sistema operacional das VMs |
| Ansible | Automação de infraestrutura |
| SSH | Administração remota |
| Nginx | Servidor web |
| Jinja2 | Templates de configuração |
| Python | Verificação de funcionamento |
| pytest | Testes automatizados |
| GitHub Actions | Integração contínua |
| Cloudflare Tunnel | Publicação segura do serviço |
| Cloudflare Access | Controle de acesso e autenticação |

## 📁 Estrutura do repositório

```text
automacao-ansible/
├── .github/
│   └── workflows/
│       └── ci.yml
├── inventory/
│   ├── hosts.ini
│   └── group_vars/
│       └── servidores.yml
├── playbooks/
│   ├── setup.yml
│   └── setup-remoto.yml
├── roles/
│   ├── common/
│   │   └── tasks/
│   │       └── main.yml
│   └── webserver/
│       ├── tasks/
│       │   └── main.yml
│       ├── handlers/
│       │   └── main.yml
│       └── templates/
│           ├── index.html.j2
│           └── nginx-site.conf.j2
├── scripts/
│   └── check_webserver.py
├── tests/
│   └── test_webserver.py
├── ansible.cfg
├── pytest.ini
└── requirements.txt
```

## ⚙️ Funcionamento do Ansible

O inventário identifica os servidores gerenciados e as variáveis de grupo definem os pacotes e parâmetros do ambiente.

**Role `common`:** realiza a configuração inicial do servidor e instala ferramentas essenciais.

**Role `webserver`:** instala o Nginx, aplica templates Jinja2, configura o virtual host e gerencia o serviço por meio de handlers.

### Executando o playbook

Em um ambiente Debian de laboratório com SSH, Ansible e permissões sudo corretamente configurados:

```bash
ansible -i inventory/hosts.ini servidores -m ansible.builtin.ping
```

Para aplicar as configurações:

```bash
ansible-playbook playbooks/setup-remoto.yml --ask-become-pass
```

O arquivo `inventory/hosts.ini` deve ser adaptado ao endereço e usuário SSH do ambiente de destino.

### Idempotência

A execução repetida do playbook não deve alterar recursos que já estejam no estado desejado.

No laboratório, uma segunda execução retornou `changed=0`, demonstrando esse comportamento para a configuração testada.

## 🧪 Testes automatizados

Os testes Python validam:

- Resposta HTTP bem-sucedida.
- Identificação correta do ambiente pelo cabeçalho `X-Lab-Environment`.
- Conteúdo esperado na página web.
- Comportamento diante de respostas incorretas.

### Preparação

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Testes simulados

```bash
python -m pytest tests/ -v -m "not integration"
```

**Resultado validado:** 3 testes aprovados.

### Teste real

```bash
python -m pytest tests/ -v -m integration
```

**Resultado validado:** 1 teste aprovado no ambiente local.

## 🔐 Segurança e acesso externo

O Nginx é disponibilizado pelo Cloudflare Tunnel e protegido por Cloudflare Access.

A aplicação utiliza dois métodos de acesso:

- **Usuários autorizados:** autenticação interativa pelo Cloudflare Access.
- **Automação:** autenticação por Service Token, com política `Service Auth`.

O teste externo utiliza as variáveis de ambiente:

```text
LAB_URL
CF_ACCESS_CLIENT_ID
CF_ACCESS_CLIENT_SECRET
```

As credenciais são armazenadas nos **GitHub Actions Secrets**, e não no código-fonte.

O ambiente de laboratório não exige abertura direta de portas de entrada no roteador para publicar o serviço via Cloudflare Tunnel.

## 🚀 CI com GitHub Actions

A pipeline possui dois jobs:

**Python Unit Tests:** executado automaticamente em pushes e pull requests para `main`, sem depender do homelab.

**Cloudflare Access Integration:** executado manualmente por `workflow_dispatch`, verificando a aplicação real usando credenciais de serviço.

Essa separação permite validar o código mesmo quando o servidor físico não está disponível.

[Visualizar execuções do GitHub Actions](https://github.com/RegisFredFilho/automacao-ansible/actions)

## 📚 Aprendizados

Este projeto permitiu praticar:

- Automação de servidores Linux.
- Administração remota via SSH.
- Organização de roles e inventários Ansible.
- Gerenciamento de serviços e configurações.
- Testes unitários e de integração.
- Separação entre ambientes locais e externos.
- Gerenciamento de credenciais.
- Integração entre infraestrutura própria e serviços em nuvem.



