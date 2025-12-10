# Utiliser une image Python de base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les dépendances et les installer
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application Streamlit
COPY ./app /app

# Exposer le port par défaut de Streamlit
EXPOSE 8501

# Commande pour démarrer l'application Streamlit
# Note : 'streamlit run' doit être la commande d'entrée (ENTRYPOINT ou CMD)
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]