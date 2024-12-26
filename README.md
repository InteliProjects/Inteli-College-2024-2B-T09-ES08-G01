# Inteli - Instituto de Tecnologia e Liderança 

<p align="center">
  <a href= "https://www.inteli.edu.br/"><img src="docs/assets/inteli.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0" width=40% height=40%></a>
</p>

<br>

# Arquitetura de Software Flexível e Sustentável

## 👨🏻‍🔧 Bobs os Construtores

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/anna-aragao">Anna Aragão</a>
- <a href="https://www.linkedin.com/in/davi-ferreira-arantes">Davi Arantes</a>
- <a href="https://www.linkedin.com/in/gabriellysilvavitor/">Gabrielly Vitor</a>
- <a href="https://www.linkedin.com/in/théo-tosto-7a0a9922b">Theo Tosto</a>
- <a href="https://www.linkedin.com/in/victor-gabriel-marques">Victor Marques</a>


## 👩‍🏫 Professores:

### Orientador(a) 
- Hermano Peixoto

### Instrutores
- José Romualdo
- Hermano Peixoto
- Francisco Escobar
- Geraldo Magela
- Lisane Valdo
- Ana Cristina dos Santos
- Reginaldo Arakaki

## 📜 Descrição

Este projeto visa desenvolver uma solução tecnológica para o Instituto de Pesquisas Tecnológicas (IPT), focada na gestão e segurança de relatórios técnicos gerados durante inspeções de obras e edificações. O sistema proposto tem como principais objetivos:

### Objetivos Principais
- Garantir o armazenamento seguro e a integridade dos dados de inspeção
- Implementar um sistema robusto de backup e recuperação de dados
- Assegurar a confidencialidade das informações através de criptografia ponta a ponta
- Fornecer alta disponibilidade e tolerância a falhas
- Facilitar o acesso e controle de versões dos relatórios técnicos

### Características Principais
- **Armazenamento Seguro**: Sistema centralizado com backup automatizado em nuvem e alta disponibilidade
- **Criptografia**: Implementação de criptografia ponta a ponta (E2EE) para garantir a confidencialidade dos dados
- **Monitoramento**: Sistema de Gerenciamento de Informações e Eventos de Segurança (SIEM) para detecção de anomalias
- **Alta Disponibilidade**: Arquitetura com redundância ativa e failover automático
- **Controle de Versões**: Sistema automatizado para rastreamento e controle de alterações nos documentos

### Tecnologias Utilizadas
- Python e Go para os serviços principais
- Node.js/TypeScript para servidores de aplicação
- NGINX para balanceamento de carga
- Sistemas de armazenamento em nuvem (Google Cloud e Backblaze)
- Docker para containerização

O sistema foi desenvolvido com foco em segurança, confiabilidade e eficiência, atendendo às necessidades específicas do IPT no setor de inspeção de obras e edificações.

## 📁 Estrutura de pastas

O diretório `/src` contém a implementação principal do sistema, organizada nos seguintes componentes:

`/backupSystem` - Sistema de Backup e Redundância
- Sistema automatizado de backup com redundância usando Google Cloud e Backblaze
- Desenvolvido em Python com integrações para armazenamento em nuvem
- Inclui testes e gerenciamento de configuração

`/e2ee` - Criptografia Ponta a Ponta
- Implementação de criptografia ponta a ponta para segurança dos dados
- Desenvolvido em Go para performance e segurança
- Inclui testes de criptografia e utilitários

`/redundance` - Sistema de Alta Disponibilidade
- Implementação de redundância de servidores e balanceamento de carga
- Servidor em Node.js/TypeScript com configuração NGINX
- Containerização Docker para escalabilidade

`/siemService` - Gerenciamento de Informações e Eventos de Segurança
- Sistema SIEM para monitoramento de segurança e detecção de anomalias
- Sistema de logs e alertas baseado em Python
- Inclui recursos de geolocalização e auditoria

`/notebooks` - Análises e Simulações
- Notebooks Jupyter para análise do sistema e simulações
- Testes de performance e visualização de métricas
- Documentação das decisões arquiteturais

Cada componente foi projetado para trabalhar em conjunto oferecendo:
- Armazenamento e transmissão segura de dados
- Alta disponibilidade através de redundância
- Monitoramento de segurança em tempo real
- Backup e recuperação automatizados

## 🔧 Instalação

Para executar este projeto, você precisará das seguintes ferramentas:

### Requisitos

1. **VSCode**
   - Baixe e instale o [Visual Studio Code](https://code.visualstudio.com/)
   - Extensões recomendadas:
     - Python
     - Go
     - Docker
     - Node.js

2. **Python**
   - Instale o Python 3.10 ou superior através do [site oficial](https://www.python.org/downloads/)


3. **Node.js**
   - Instale o Node.js LTS (18.x ou superior) do [site oficial](https://nodejs.org/)


4. **Docker**
   - Instale o Docker Desktop para [Windows](https://docs.docker.com/desktop/install/windows/) ou [Mac](https://docs.docker.com/desktop/install/mac/)
   - Para Linux, siga as instruções para sua distribuição na [documentação oficial](https://docs.docker.com/engine/install/)


5. **Go**
   - Baixe e instale o Go do [site oficial](https://go.dev/dl/)


## 🗃 Histórico de lançamentos

Para acessar o histórico de lançamentos, clique [aqui](https://github.com/Inteli-College/2024-2B-T09-ES08-G01/releases).


## 📋 Licença/License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Inteli-College/2024-2B-T09-ES08-G01">Arquitetura de Software Flexível e Sustentável</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://www.inteli.edu.br/">INTELI</a>, <a href="https://www.linkedin.com/in/anna-aragao">Anna Aragão</a>, <a href="https://www.linkedin.com/in/davi-ferreira-arantes">Davi Arantes</a>, <a href="https://www.linkedin.com/in/gabriellysilvavitor/">Gabrielly Vitor</a>, <a href="https://www.linkedin.com/in/théo-tosto-7a0a9922b">Theo Tosto</a>, <a href="https://www.linkedin.com/in/victor-gabriel-marques">Victor Marques</a>, is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a></p>
