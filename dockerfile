# Usar uma imagem base com Python
FROM python:3.10-slim

# Instalar dependências do sistema necessárias para o PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt requirements.txt

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto
COPY . .

# Expor a porta que a aplicação usa
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "app.py"]