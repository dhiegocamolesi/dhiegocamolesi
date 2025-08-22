# Projeto IBGE - Extração, Normalização e Armazenamento de Indicadores

Este projeto realiza a extração de indicadores da **API de Países do IBGE**, com base em uma lista pré-definida de paíse alvo, normaliza os dados e armazena os resultados em um banco de dados **PostgreSQL**.


# Como construir e executar o projeto com Docker

O projeto pode ser executado em Container Docker, sem precisar instalar Python e dependências na máquina local.

### 1. Clonar o repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <PASTA_DO_REPOSITORIO>
```
### 2. Construir a imagem
  Na raiz do projeto (onde estão Dockerfile, requirements.txt e TesteDadosIBGE.py), execute:

```bash
docker build -t projeto-ibge .
```
Isso cria a imagem chamada `projeto-ibge`.

### 3. Executar o container
  Para rodar o script, conectando ao PostgreSQL local ou remoto, use:

```bash
docker run --rm   -e DB_USER=postgres   -e DB_PASS=teste123   -e DB_HOST=host.docker.internal   -e DB_PORT=5432   -e DB_NAME=db_ibge   projeto-ibge
```
# > Observação:  
> - Use `host.docker.internal` no **DB_HOST** quando o PostgreSQL estiver instalado na sua máquina.  
> - Se o PostgreSQL estiver em outro servidor, substitua pelo IP ou hostname correspondente.  
> - Certifique-se de que o banco 'db_ibge' já existe.  

### 4. Verificando os dados
  Após a execução, conecte ao PostgreSQL e verifique as tabelas criadas:

```sql
\c db_ibge;
\d
SELECT * FROM chegada_turistas LIMIT 10;
```

---

# Bibliotecas utilizadas

**requests** → Requisições HTTP para a API do IBGE
**pandas** → Manipulação e normalização dos dados
**sqlalchemy** → Conexão e escrita no PostgreSQL
**datetime e time** → Manipulação de datas e controle de tentativas

---

# Observações Técnicas Relevantes

Tratamento de erros de rede → uso de try/except com raise_for_status() para capturar falhas HTTP e evitar dados corrompidos.

Logs básicos no console → cada etapa (extração, normalização, salvamento) imprime mensagens para fácil acompanhamento.

Flexibilidade de configuração → credenciais e parâmetros de conexão são definidos via variáveis de ambiente, facilitando a portabilidade.

Normalização de dados complexos → transforma o JSON aninhado da API do IBGE em uma tabela relacional limpa.

Deduplicação de registros → garante que apenas um valor por indicador + país + ano seja armazenado.

Validação de consistência → exclui anos fora de intervalo válido e valores anômalos (negativos ou absurdamente altos).

Escalabilidade → o código permite adicionar novos indicadores facilmente no dicionário INDICADORES_ID.

Uso de índices únicos no banco → melhora a performance em consultas e impede duplicidade.

Compatibilidade com Docker → projeto pode ser facilmente containerizado.

Timeout configurado nas requisições (timeout=6) → evita travamento em chamadas lentas.

Boa prática de backoff exponencial → controla tentativas e reduz sobrecarga no servidor IBGE.
