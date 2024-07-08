module.exports = {
  apps: [
    {
      name: 'flask',
      script: 'gunicorn',
      args: '--bind=0.0.0.0:8000 backend:app',
      cwd: '/home/site/wwwroot',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production'
      },
      output: '/home/site/wwwroot/logs/flask.log',
      error: '/home/site/wwwroot/logs/flask_err.log'
    },
    {
      name: 'streamlit',
      script: 'streamlit',
      args: 'run app.py --server.port 8501 --server.headless true',
      cwd: '/home/site/wwwroot',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production'
      },
      output: '/home/site/wwwroot/logs/streamlit.log',
      error: '/home/site/wwwroot/logs/streamlit_err.log'
    }
  ]
};
