# AI Sales Backend API

API backend desenvolvida em Python com FastAPI, focada na simulação de um sistema de vendas com regras de negócio reais e integração com Inteligência Artificial.

## 🚀 Tecnologias Utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- OpenAI API
- Uvicorn
- dotenv

---

# 📌 Funcionalidades

## 👥 Clientes
- Cadastro de clientes
- Listagem de clientes
- Atualização de clientes
- Remoção de clientes

## 📦 Produtos
- Cadastro de produtos
- Controle de estoque
- Atualização de produtos
- Remoção de produtos

## 🛒 Pedidos
- Criação de pedidos com múltiplos itens
- Validação automática de estoque
- Atualização automática do estoque
- Cálculo automático do valor total
- Cancelamento de pedidos com rollback de estoque

## 📊 Relatórios
- Total vendido
- Produto mais vendido

## 🤖 Inteligência Artificial
- Endpoint para perguntas inteligentes sobre os dados do sistema
- Integração com OpenAI
- Respostas contextualizadas usando dados reais do banco
- Histórico de perguntas e respostas da IA

---

# 🧠 Arquitetura do Projeto

O projeto utiliza arquitetura modular:


app/
│
├── models/
├── routers/
├── schemas/
├── service/
├── database.py
└── main.py

Separação entre:

Models
Schemas
Services
Routers
⚙️ Instalação
Clone o projeto
git clone https://github.com/davizeds/ai-sales-backend-api.git
Entre na pasta
cd ai-sales-backend-api
Instale as dependências
uv sync
🔑 Variáveis de Ambiente

Crie um arquivo .env

OPENAI_API_KEY=sua_chave_aqui
▶️ Executando o Projeto
uv run uvicorn app.main:app --reload

Servidor:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs
🤖 Exemplo IA
Endpoint
POST /ia/perguntar
Body
{
  "pergunta": "qual produto mais vendido?"
}
Resposta
{
  "resposta": "O produto mais vendido foi o produto de id 1 com 15 unidades vendidas."
}
📜 Histórico da IA
Endpoint
GET /ia/historico
📈 Próximos Passos
Frontend em React
Dashboard administrativo
Autenticação JWT
Cache com Redis
Docker
Deploy em cloud
IA com análise avançada de vendas
👨‍💻 Autor

Davi Felipe Nasario

LinkedIn:
www.linkedin.com/in/davi-felipe-nasario

GitHub:
https://github.com/davizeds
