# 🛠️ Web Scraping + Hadoop MapReduce

Projeto que realiza scraping de dados da web usando Python (Selenium) e os processa com Hadoop MapReduce. Tudo automatizado com Docker e Docker Compose.

---

## 🎓 Informações Acadêmicas

Este projeto faz parte da disciplina de **Big Data** do curso de **Especialização em Engenharia de Software com DevOps** da **Universidade Estadual do Ceará - UECE**.

- **Alunos:** Ezemir Sabino e Marcos Eduardo  
- **Professor:** Denis Sousa

---

## 🚀 Tecnologias Utilizadas

- **Python 3 + Selenium**: para web scraping  
- **Apache Hadoop (HDFS + YARN + MapReduce)**: para processamento distribuído  
- **Java**: job MapReduce compilado em um `.jar`  
- **Docker + Docker Compose**: para orquestração dos serviços  

---

## 📦 Etapas do Processo

### 1. Web Scraping

Antes de subir os containers, execute o script de scraping:

```bash
python webscraping.py
```

Esse script salva arquivos `.csv` na pasta `/data/csv`.

---

### 2. Subir o ambiente completo

Tudo é automatizado a partir daqui. Basta rodar:

```bash
docker-compose up --build
```

Isso irá:

- Subir os serviços Hadoop (NameNode, DataNode, ResourceManager etc)
- Criar automaticamente diretórios no HDFS
- Carregar os arquivos CSV gerados pelo scraper
- Executar o Job Hadoop MapReduce (`job.jar`)
- Salvar os resultados em `/data/output` no HDFS

---

## 📁 Estrutura Esperada no HDFS

```
/data/input     ← arquivos CSV carregados  
/data/output    ← resultado do Job MapReduce
```

---

## 📌 Observações

- O `geckodriver.exe` já está incluído no projeto. Apenas certifique-se de ter o Firefox instalado.  
- O Job Java já está compilado como `job.jar` e é executado automaticamente pelo serviço `init-hdfs`.  
- As configurações do Hadoop estão na pasta `config/`.

---

## ✅ Verificando os Resultados

Você pode acessar a UI do Hadoop para acompanhar o processamento:

- **NameNode UI:** http://localhost:9870  
- **ResourceManager UI:** http://localhost:8088  
- **HistoryServer:** http://localhost:8188

---

## 🔁 Reexecutar o Job

Para rodar o job novamente (por exemplo, após novo scraping), basta:

```bash
docker-compose restart init-hdfs
```

---

## 📄 Licença

Distribuído sob a licença MIT. Livre para usar, estudar e modificar.

---

> Projeto criado para fins didáticos envolvendo Big Data, automação e processamento distribuído com MapReduce.