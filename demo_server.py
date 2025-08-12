#!/usr/bin/env python3
"""
Book2Video Demo Server - Teste Super Fácil
Roda com Python padrão, sem dependências externas
Simula todo o sistema Book2Video funcionando
"""

import http.server
import socketserver
import json
import urllib.parse
import time
import uuid
from datetime import datetime
import os

# Dados em memória para o demo
users = {}
projects = {}
sessions = {}

class Book2VideoHandler(http.server.SimpleHTTPRequestHandler):
    """Handler customizado para simular a API Book2Video"""
    
    def do_GET(self):
        """Handle GET requests"""
        path = self.path.split('?')[0]
        
        if path == '/':
            self.serve_homepage()
        elif path == '/health':
            self.serve_health()
        elif path == '/stats':
            self.serve_stats()
        elif path == '/demo':
            self.serve_demo_page()
        elif path == '/projects':
            self.serve_projects()
        elif path.startswith('/projects/'):
            project_id = path.split('/')[-1]
            self.serve_project_detail(project_id)
        else:
            self.serve_404()
    
    def do_POST(self):
        """Handle POST requests"""
        path = self.path.split('?')[0]
        
        if path == '/auth/register':
            self.handle_register()
        elif path == '/auth/login':
            self.handle_login()
        elif path == '/projects/upload':
            self.handle_upload()
        elif path.startswith('/projects/') and path.endswith('/process'):
            project_id = path.split('/')[-2]
            self.handle_process(project_id)
        else:
            self.serve_404()
    
    def serve_homepage(self):
        """Serve the main demo page"""
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚🎬 Book2Video Demo</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', sans-serif; 
            margin: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 40px; 
        }}
        .card {{ 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; 
            padding: 30px; 
            margin: 20px 0; 
            backdrop-filter: blur(10px);
        }}
        .button {{ 
            background: #4CAF50; 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            cursor: pointer; 
            margin: 10px; 
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }}
        .button:hover {{ 
            background: #45a049; 
            transform: translateY(-2px);
        }}
        .status {{ 
            background: rgba(76, 175, 80, 0.2); 
            border-left: 4px solid #4CAF50; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 5px;
        }}
        .features {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin: 30px 0; 
        }}
        .feature {{ 
            background: rgba(255,255,255,0.05); 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
        }}
        .api-section {{ 
            background: rgba(0,0,0,0.2); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
        }}
        .endpoint {{ 
            background: rgba(255,255,255,0.1); 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 5px; 
            font-family: monospace;
        }}
        .demo-upload {{ 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
        }}
        input[type="file"], input[type="text"] {{ 
            background: rgba(255,255,255,0.9); 
            color: #333; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            margin: 10px 0; 
            width: 100%;
            max-width: 400px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚🎬 Book2Video Demo System</h1>
            <p>Sistema completo funcionando - Converte livros em vídeos com IA</p>
        </div>
        
        <div class="status">
            <h3>✅ Sistema Online e Funcionando!</h3>
            <p><strong>Tempo online:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Usuários registrados:</strong> {len(users)}</p>
            <p><strong>Projetos criados:</strong> {len(projects)}</p>
            <p><strong>Status:</strong> 🟢 Operacional</p>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🤖 IA Avançada</h3>
                <p>OpenAI GPT-4 + ElevenLabs</p>
                <p>Converte texto em cenas cinematográficas</p>
            </div>
            <div class="feature">
                <h3>🎬 Vídeos Profissionais</h3>
                <p>FFmpeg + Pipeline automático</p>
                <p>MP4 com narração e imagens</p>
            </div>
            <div class="feature">
                <h3>📊 Monitoramento</h3>
                <p>Grafana + Prometheus</p>
                <p>Métricas em tempo real</p>
            </div>
        </div>
        
        <div class="card">
            <h2>🧪 Testar Sistema</h2>
            <p>Escolha como quer testar o Book2Video:</p>
            
            <a href="/demo" class="button">📱 Interface Demo</a>
            <a href="/health" class="button">🔍 Health Check</a>
            <a href="/stats" class="button">📊 Estatísticas</a>
            <a href="/projects" class="button">📋 Ver Projetos</a>
        </div>
        
        <div class="api-section">
            <h2>🔌 API Endpoints Disponíveis</h2>
            <div class="endpoint">GET /health - Verificar saúde do sistema</div>
            <div class="endpoint">POST /auth/register - Registrar usuário</div>
            <div class="endpoint">POST /auth/login - Login usuário</div>
            <div class="endpoint">POST /projects/upload - Upload de livro</div>
            <div class="endpoint">POST /projects/{{id}}/process - Processar com IA</div>
            <div class="endpoint">GET /projects - Listar projetos</div>
            <div class="endpoint">GET /stats - Estatísticas do sistema</div>
        </div>
        
        <div class="demo-upload">
            <h2>📁 Demo Upload Rápido</h2>
            <p>Simule um upload de livro:</p>
            <form onsubmit="demoUpload(event)">
                <input type="text" placeholder="Título do livro" id="title" value="O Pequeno Príncipe"><br>
                <input type="file" accept=".txt,.pdf,.docx" id="file"><br>
                <button type="submit" class="button">🚀 Processar com IA</button>
            </form>
            <div id="result"></div>
        </div>
    </div>
    
    <script>
        async function demoUpload(event) {{
            event.preventDefault();
            
            const result = document.getElementById('result');
            result.innerHTML = '<p>🤖 Processando com IA...</p>';
            
            // Simular processamento
            setTimeout(() => {{
                const projectId = Math.random().toString(36).substr(2, 9);
                result.innerHTML = `
                    <div style="background: rgba(76, 175, 80, 0.2); padding: 15px; border-radius: 5px; margin: 10px 0;">
                        <h3>✅ Processamento Concluído!</h3>
                        <p><strong>Projeto ID:</strong> ${{projectId}}</p>
                        <p><strong>Cenas geradas:</strong> 4 cenas</p>
                        <p><strong>Duração:</strong> 3 minutos 27 segundos</p>
                        <p><strong>Custo:</strong> $0.12</p>
                        <p><strong>Qualidade:</strong> 9.2/10</p>
                        <p><strong>Status:</strong> 🎬 Vídeo pronto!</p>
                        <a href="/projects/${{projectId}}" class="button">👀 Ver Detalhes</a>
                    </div>
                `;
            }}, 3000);
        }}
        
        // Auto-refresh stats
        setInterval(() => {{
            const time = document.querySelector('.status p strong');
            if (time) {{
                time.nextSibling.textContent = ' ' + new Date().toLocaleTimeString();
            }}
        }}, 1000);
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_health(self):
        """Health check endpoint"""
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": "demo",
            "services": {
                "database": "healthy",
                "redis": "healthy", 
                "openai": "demo_mode"
            },
            "uptime_seconds": int(time.time() - server_start_time),
            "demo_mode": True
        }
        
        self.send_json_response(health_data)
    
    def serve_stats(self):
        """System statistics"""
        stats = {
            "total_users": len(users),
            "total_projects": len(projects),
            "completed_projects": len([p for p in projects.values() if p.get('status') == 'completed']),
            "success_rate": 95.7,
            "system_status": "operational",
            "version": "1.0.0",
            "uptime": "running",
            "demo_mode": True,
            "processing_queue": 0,
            "average_processing_time": 127,
            "total_videos_generated": 42,
            "ai_cost_savings": "78%"
        }
        
        self.send_json_response(stats)
    
    def serve_demo_page(self):
        """Demo interface page"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>📱 Book2Video Interface Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .result { background: #e8f5e8; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .processing { background: #fff3cd; padding: 15px; margin: 15px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 Book2Video - Interface Demo</h1>
        <p>Interface simulada do sistema completo</p>
        
        <h3>🔐 1. Autenticação</h3>
        <button onclick="demoLogin()" class="button">Login Demo</button>
        <div id="auth-result"></div>
        
        <h3>📁 2. Upload de Livro</h3>
        <input type="file" id="book-file" accept=".txt,.pdf,.docx">
        <button onclick="demoUpload()" class="button">Upload</button>
        <div id="upload-result"></div>
        
        <h3>🤖 3. Processamento IA</h3>
        <button onclick="demoProcess()" class="button">Processar com IA</button>
        <div id="process-result"></div>
        
        <h3>📊 4. Status do Sistema</h3>
        <button onclick="loadStats()" class="button">Ver Estatísticas</button>
        <div id="stats-result"></div>
    </div>
    
    <script>
        function demoLogin() {
            document.getElementById('auth-result').innerHTML = '<div class="result">✅ Login realizado com sucesso!<br>Token: demo_token_123</div>';
        }
        
        function demoUpload() {
            document.getElementById('upload-result').innerHTML = '<div class="result">✅ Livro enviado com sucesso!<br>Projeto ID: proj_demo_456</div>';
        }
        
        function demoProcess() {
            const result = document.getElementById('process-result');
            result.innerHTML = '<div class="processing">🤖 Processando com IA GPT-4...</div>';
            
            setTimeout(() => {
                result.innerHTML = `
                    <div class="result">
                        ✅ Processamento concluído!<br>
                        🎬 4 cenas geradas<br>
                        ⏱️ Tempo: 2min 34s<br>
                        💰 Custo: $0.15<br>
                        📊 Qualidade: 9.1/10
                    </div>
                `;
            }, 3000);
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const stats = await response.json();
                document.getElementById('stats-result').innerHTML = `
                    <div class="result">
                        📊 Estatísticas do Sistema:<br>
                        👥 Usuários: ${stats.total_users}<br>
                        📋 Projetos: ${stats.total_projects}<br>
                        ✅ Taxa sucesso: ${stats.success_rate}%<br>
                        🎬 Vídeos gerados: ${stats.total_videos_generated}<br>
                        💰 Economia IA: ${stats.ai_cost_savings}
                    </div>
                `;
            } catch(e) {
                document.getElementById('stats-result').innerHTML = '<div class="result">Carregando estatísticas...</div>';
            }
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_projects(self):
        """List projects"""
        project_list = []
        for pid, project in projects.items():
            project_list.append({
                "id": pid,
                "title": project.get("title", "Untitled"),
                "status": project.get("status", "uploaded"),
                "created_at": project.get("created_at", datetime.now().isoformat())
            })
        
        self.send_json_response(project_list)
    
    def serve_project_detail(self, project_id):
        """Project detail"""
        if project_id in projects:
            project = projects[project_id]
            self.send_json_response(project)
        else:
            # Create demo project
            demo_project = {
                "id": project_id,
                "title": "Demo Project - O Pequeno Príncipe", 
                "status": "completed",
                "original_filename": "pequeno_principe.txt",
                "file_size_bytes": 15420,
                "target_duration_minutes": 3,
                "visual_style": "educational",
                "video_url": "https://demo.book2video.com/videos/demo.mp4",
                "thumbnail_url": "https://demo.book2video.com/thumbs/demo.jpg",
                "processing_time_seconds": 127,
                "quality_rating": 9.2,
                "cost_usd": 0.12,
                "scenes": [
                    {
                        "scene_number": 1,
                        "narration": "Em um pequeno planeta, não maior que uma casa, vivia um pequeno príncipe...",
                        "visual_description": "Um pequeno asteroide flutuando no espaço com uma figura pequena e uma única rosa",
                        "duration_seconds": 45,
                        "emotional_tone": "contemplativo"
                    },
                    {
                        "scene_number": 2,
                        "narration": "O pequeno príncipe aprendeu com uma sábia raposa que o essencial é invisível aos olhos...",
                        "visual_description": "Uma raposa dourada e o pequeno príncipe sentados juntos em um campo ao pôr do sol",
                        "duration_seconds": 52,
                        "emotional_tone": "inspirador"
                    }
                ],
                "created_at": datetime.now().isoformat(),
                "demo_mode": True
            }
            self.send_json_response(demo_project)
    
    def handle_register(self):
        """Handle user registration"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_id = str(uuid.uuid4())
                users[user_id] = {
                    "id": user_id,
                    "email": data.get("email", "demo@book2video.com"),
                    "full_name": data.get("full_name", "Demo User"),
                    "subscription_tier": "free",
                    "created_at": datetime.now().isoformat()
                }
                self.send_json_response(users[user_id])
            except:
                self.send_json_response({"error": "Invalid data"}, 400)
        else:
            self.send_json_response({"error": "No data"}, 400)
    
    def handle_login(self):
        """Handle user login"""
        response = {
            "access_token": "demo_token_" + str(int(time.time())),
            "token_type": "bearer",
            "user": {
                "id": "demo_user_123",
                "email": "demo@book2video.com",
                "full_name": "Demo User",
                "subscription_tier": "free",
                "created_at": datetime.now().isoformat()
            }
        }
        self.send_json_response(response)
    
    def handle_upload(self):
        """Handle file upload"""
        project_id = str(uuid.uuid4())
        projects[project_id] = {
            "id": project_id,
            "title": "Demo Upload Project",
            "status": "uploaded",
            "file_size": 12500,
            "created_at": datetime.now().isoformat()
        }
        
        response = {
            "message": "File uploaded successfully",
            "project_id": project_id,
            "status": "uploaded",
            "file_size": 12500,
            "processing_started": True
        }
        self.send_json_response(response)
    
    def handle_process(self, project_id):
        """Handle AI processing"""
        if project_id not in projects:
            projects[project_id] = {"id": project_id, "title": "Demo Project"}
        
        # Update project status
        projects[project_id].update({
            "status": "completed",
            "processing_time_seconds": 127,
            "cost_usd": 0.12,
            "scenes_generated": 4,
            "quality_rating": 9.1
        })
        
        response = {
            "message": "AI processing completed successfully",
            "project_id": project_id,
            "status": "completed",
            "processing_time_seconds": 127,
            "total_duration_seconds": 207,
            "scenes_generated": 4,
            "cost_usd": 0.12,
            "book_analysis": {
                "title": "Demo Book",
                "word_count": 1250,
                "estimated_reading_time_minutes": 6,
                "chapters_detected": 3
            },
            "demo_mode": True
        }
        self.send_json_response(response)
    
    def serve_404(self):
        """Serve 404 page"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <html><body>
        <h1>404 - Endpoint não encontrado</h1>
        <p><a href="/">← Voltar para página inicial</a></p>
        </body></html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        self.wfile.write(json_data.encode('utf-8'))

def start_demo_server():
    """Start the demo server"""
    global server_start_time
    server_start_time = time.time()
    
    PORT = 8000
    
    print("🚀 BOOK2VIDEO DEMO SERVER")
    print("=" * 40)
    print(f"🌐 Servidor iniciado em: http://localhost:{PORT}")
    print(f"📱 Interface principal: http://localhost:{PORT}/")
    print(f"🔍 Health check: http://localhost:{PORT}/health")
    print(f"📊 Estatísticas: http://localhost:{PORT}/stats")
    print(f"🧪 Demo interface: http://localhost:{PORT}/demo")
    print("=" * 40)
    print("✅ Sistema Book2Video funcionando!")
    print("🤖 Simula todo o pipeline: Upload → IA → Vídeo")
    print("⏹️  Pressione Ctrl+C para parar")
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), Book2VideoHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Servidor parado pelo usuário")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Porta {PORT} já está em uso")
            print("💡 Feche outros serviços ou use outra porta")
        else:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    start_demo_server()