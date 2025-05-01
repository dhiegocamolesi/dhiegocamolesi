# Windfarm - Projeto de Coleta e Processamento de Dados em Tempo Real

O projeto **Windfarm** simula a coleta e processamento de dados de turbinas eólicas em tempo real. Utilizando os serviços da AWS, o fluxo de dados é gerenciado de forma eficiente com Kinesis Data Streams, S3, Glue, Athena e outros componentes para criar uma solução robusta e escalável.

## Visão Geral

O objetivo do projeto é criar um fluxo de dados em tempo real, onde três aplicações geradoras de dados enviam informações para o AWS Kinesis Data Stream. Estes dados são armazenados no S3, processados e armazenados no banco de dados AWS Glue, e podem ser consultados via Athena. O processo é automatizado usando Kinesis Firehouse para entrega, Crawler e Catalog para criação de schemas, e Jobs.

## Arquitetura do Sistema

1. **AWS Kinesis Data Stream**: Coleta dados em tempo real de dispositivos simulados (turbinas eólicas).
2. **AWS S3**: Armazena os dados coletados de forma durável e segura.
3. **AWS IAM**: Função com persmissão para o GLUE.
4. **AWS Kinesis Data Firehouse**: Realiza a entrega dos dados particionados por data para o destino final (S3).
5. **AWS Crawler e Catalog**: Cria e mantém os schemas para os dados armazenados no S3.
6. **AWS Glue**: Processa e organiza os dados para análise posterior.
7. **AWS Athena**: Permite consultas SQL diretamente nos dados processados.

## Tecnologias Utilizadas

- **AWS Kinesis Data Stream**: Para coleta de dados em tempo real.
- **AWS S3 Bucket**: Para armazenamento dos dados brutos.
- **AWS Kinesis Data Firehouse**: Para entrega contínua dos dados.
- **AWS Crawler e Catalog**: Para gerenciamento e criação de schemas.
- **AWS Glue**: Para processamento e armazenamento de dados.
- **AWS Athena**: Para execução de consultas SQL sobre os dados armazenados.

## Funcionalidades do Projeto

- **Coleta de Dados**: Três aplicações geradoras de dados simulam as turbinas eólicas e enviam as informações para o Kinesis Data Stream.
- **Armazenamento no S3**: Dados coletados são automaticamente armazenados no S3.
- **Processamento no Glue**: AWS Glue organiza os dados e os armazena em um formato otimizado para consulta.
- **Consulta de Dados**: Dados podem ser consultados facilmente com o AWS Athena.

## Como Configurar

### Requisitos

- Conta AWS configurada com as permissões adequadas.
- Python 3.x instalado.
- Acesso aos serviços AWS mencionados.


