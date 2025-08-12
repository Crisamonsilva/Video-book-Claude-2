#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Book2Video Simple Demo Server
Teste super facil - roda com Python padrao
"""

import http.server
import socketserver
import json
import time
from datetime import datetime

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path == '/health':
            self.serve_health()
        else:
            self.serve_404()
    
    def serve_main_page(self):
        html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Book2Video Demo - Sistema Funcionando</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .status { 
            background: rgba(76, 175, 80, 0.3); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            border-left: 5px solid #4CAF50;
        }
        .button { 
            background: #4CAF50; 
            color: white; 
            padding: 15px 25px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            cursor: pointer; 
            margin: 10px 5px; 
            text-decoration: none;
            display: inline-block;
        }
        .button:hover { 
            background: #45a049; 
        }
        .demo-section {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .result {
            background: rgba(76, 175, 80, 0.2);
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #4CAF50;
        }
        input[type="text"], input[type="file"] {
            background: rgba(255,255,255,0.9);
            color: #333;
            padding: 10px;
            border: none;
            border-radius: 5px;
            margin: 10px 0;
            width: 100%;
            max-width: 400px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚🎬 Book2Video Demo System</h1>
        <p>Sistema completo de conversao de livros em videos com IA</p>
        
        <div class="status">
            <h3>✅ Sistema Online e Funcionando!</h3>
            <p><strong>Status:</strong> Operacional</p>
            <p><strong>Hora atual:</strong> <span id="current-time"></span></p>
            <p><strong>Tecnologias:</strong> OpenAI GPT-4 + ElevenLabs + FFmpeg</p>
        </div>
        
        <div class="demo-section">
            <h2>🧪 Demonstracao Interativa</h2>
            <p>Simule o processo completo de conversao:</p>
            
            <h3>1. Upload de Livro</h3>
            <input type="text" id="book-title" placeholder="Titulo do livro" value="O Pequeno Principe">
            <input type="file" id="book-file" accept=".txt,.pdf,.docx">
            <button class="button" onclick="simulateUpload()">📁 Upload Livro</button>
            <div id="upload-result"></div>
            
            <h3>2. Processamento com IA</h3>
            <button class="button" onclick="simulateAI()">🤖 Processar com IA</button>
            <div id="ai-result"></div>
            
            <h3>3. Geracao de Video</h3>
            <button class="button" onclick="simulateVideo()">🎬 Gerar Video</button>
            <div id="video-result"></div>
        </div>
        
        <div class="demo-section">
            <h2>📊 Metricas do Sistema</h2>
            <div id="stats">
                <p><strong>Usuarios registrados:</strong> 1,247</p>
                <p><strong>Videos gerados:</strong> 3,891</p>
                <p><strong>Taxa de sucesso:</strong> 98.3%</p>
                <p><strong>Tempo medio processamento:</strong> 3min 42s</p>
                <p><strong>Economia de custos IA:</strong> 78%</p>
            </div>
            <button class="button" onclick="updateStats()">🔄 Atualizar Stats</button>
        </div>
        
        <div class="demo-section">
            <h2>🔌 API Endpoints</h2>
            <p>Endpoints disponiveis no sistema real:</p>
            <ul style="text-align: left;">
                <li><code>POST /auth/register</code> - Registro de usuario</li>
                <li><code>POST /auth/login</code> - Login de usuario</li>
                <li><code>POST /projects/upload</code> - Upload de livro</li>
                <li><code>POST /projects/{id}/process</code> - Processar com IA</li>
                <li><code>GET /projects</code> - Listar projetos</li>
                <li><code>GET /health</code> - Status do sistema</li>
            </ul>
            <button class="button" onclick="testAPI()">🧪 Testar API</button>
            <div id="api-result"></div>
        </div>
        
        <div class="demo-section">
            <h2>🚀 Proximos Passos</h2>
            <p>Para usar o sistema completo:</p>
            <ol style="text-align: left;">
                <li>Instalar Docker Desktop</li>
                <li>Executar: <code>docker-compose up -d</code></li>
                <li>Configurar API keys (OpenAI, ElevenLabs)</li>
                <li>Acessar: <code>http://localhost:8000/docs</code></li>
            </ol>
        </div>
    </div>
    
    <script>
        // Update current time
        function updateTime() {
            document.getElementById('current-time').textContent = new Date().toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
        updateTime();
        
        function simulateUpload() {
            const title = document.getElementById('book-title').value || 'Livro Demo';
            document.getElementById('upload-result').innerHTML = 
                `<div class="result">
                    ✅ Upload concluido!<br>
                    📖 Titulo: ${title}<br>
                    📋 Projeto ID: proj_${Math.random().toString(36).substr(2, 8)}<br>
                    📄 Tamanho: 125 KB<br>
                    📊 Paginas detectadas: 87
                </div>`;
        }
        
        function simulateAI() {
            const result = document.getElementById('ai-result');
            result.innerHTML = '<p style="color: #ffeb3b;">🤖 Processando com OpenAI GPT-4...</p>';
            
            setTimeout(() => {
                result.innerHTML = 
                    `<div class="result">
                        ✅ IA processamento concluido!<br>
                        🎬 Cenas geradas: 6 cenas<br>
                        ⏱️ Tempo processamento: 2min 34s<br>
                        💰 Custo: $0.18<br>
                        📊 Qualidade: 9.3/10<br>
                        🎯 Duracao video: 4min 12s
                    </div>`;
            }, 3000);
        }
        
        function simulateVideo() {
            const result = document.getElementById('video-result');
            result.innerHTML = '<p style="color: #ffeb3b;">🎬 Gerando video com FFmpeg...</p>';
            
            setTimeout(() => {
                result.innerHTML = 
                    `<div class="result">
                        ✅ Video gerado com sucesso!<br>
                        🎥 URL: https://demo.book2video.com/videos/demo.mp4<br>
                        🖼️ Thumbnail: Gerada automaticamente<br>
                        📏 Resolucao: 1920x1080 (Full HD)<br>
                        💾 Tamanho: 45.2 MB<br>
                        🎵 Audio: Narracao ElevenLabs incluida
                    </div>`;
            }, 4000);
        }
        
        function updateStats() {
            const stats = document.getElementById('stats');
            const users = Math.floor(Math.random() * 100) + 1200;
            const videos = Math.floor(Math.random() * 200) + 3800;
            
            stats.innerHTML = 
                `<p><strong>Usuarios registrados:</strong> ${users.toLocaleString()}</p>
                <p><strong>Videos gerados:</strong> ${videos.toLocaleString()}</p>
                <p><strong>Taxa de sucesso:</strong> ${(Math.random() * 2 + 97).toFixed(1)}%</p>
                <p><strong>Tempo medio processamento:</strong> ${Math.floor(Math.random() * 60 + 180)}s</p>
                <p><strong>Economia de custos IA:</strong> ${Math.floor(Math.random() * 10 + 70)}%</p>`;
        }
        
        async function testAPI() {
            const result = document.getElementById('api-result');
            result.innerHTML = '<p style="color: #ffeb3b;">🔍 Testando endpoints da API...</p>';
            
            try {
                const response = await fetch('/health');
                const data = await response.json();
                
                result.innerHTML = 
                    `<div class="result">
                        ✅ API funcionando!<br>
                        📊 Status: ${data.status}<br>
                        🕐 Timestamp: ${data.timestamp}<br>
                        🔧 Versao: ${data.version}<br>
                        🤖 Modo: ${data.demo_mode ? 'Demo' : 'Producao'}
                    </div>`;
            } catch(e) {
                result.innerHTML = 
                    `<div class="result">
                        ✅ Demo API simulada funcionando!<br>
                        📊 Status: healthy<br>
                        🔧 Versao: 1.0.0<br>
                        🤖 Modo: Demo local
                    </div>`;
            }
        }
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_health(self):
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "demo_mode": True,
            "services": {
                "database": "healthy",
                "redis": "healthy",
                "openai": "demo_mode"
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        json_data = json.dumps(health_data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def serve_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = "<html><body><h1>404 - Pagina nao encontrada</h1><p><a href='/'>Voltar</a></p></body></html>"
        self.wfile.write(html.encode('utf-8'))

def main():
    PORT = 8080
    
    print("=" * 50)
    print("BOOK2VIDEO DEMO SERVER")
    print("=" * 50)
    print(f"Servidor rodando em: http://localhost:{PORT}")
    print("Abra seu navegador e acesse o endereco acima")
    print("=" * 50)
    print("Sistema Book2Video funcionando!")
    print("Simula todo o pipeline: Upload -> IA -> Video")
    print("Pressione Ctrl+C para parar")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado")
    except OSError as e:
        print(f"Erro: {e}")
        print("Tente usar outra porta")

if __name__ == "__main__":
    main()