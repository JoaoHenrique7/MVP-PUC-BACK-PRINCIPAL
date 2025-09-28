# Documentação do Projeto: Gerenciador de Endereços

## Visão Geral
Sistema composto por dois repositórios:
1. **Backend**: API em Flask que consulta a ViaCEP, salva dados em SQLite e oferece CRUD completo.
2. **Frontend**: Aplicação React + TypeScript + Vite que consome a API e permite gerenciar endereços.

Arquitetura:
- Frontend (React TSX) → chama API Flask → consulta ViaCEP → salva dados no SQLite
- Comunicação via HTTP REST

---

# Backend

## Tecnologias
- Python 3.11+
- Flask
- Flask-CORS
- Flask-RESTX (Swagger)
- Requests
- SQLite

## Instalação Local
```bash
git clone https://github.com/JoaoHenrique7/MVP-PUC-BACK-PRINCIPAL.git
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
A API estará disponível em: `http://localhost:5000`
Swagger UI: `http://localhost:5000/`

## Rodando com Docker
```bash
docker build -t backend-enderecos .
docker run -p 5000:5000 backend-enderecos
```
Ou com docker-compose:
```bash
docker compose up
```

## Rotas
| Método | Rota | Descrição |
|--------|------|-----------|
| GET    | /enderecos | Lista todos os endereços |
| POST   | /enderecos | Adiciona um endereço via CEP |
| PUT    | /enderecos/{id} | Atualiza endereço pelo ID |
| DELETE | /enderecos/{id} | Deleta endereço pelo ID |
