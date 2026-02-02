# Desafio 4 - API e Interface Web

Este projeto consiste em uma plataforma de visualização de dados da ANS, composta por um backend robusto em Python e um frontend moderno e reativo em Vue.js 3.

## 🚀 Tecnologias Utilizadas
- **Backend**: FastAPI, SQLite, Pydantic, Uvicorn.
- **Frontend**: Vue.js 3 (Composition API), Vite, Pinia, Vue Router, Axios, Chart.js, Lucide Icons.

---

## 🛠️ Justificativas e Trade-offs: Backend

### 4.2.1. Escolha do Framework: Option B (FastAPI)
- **Justificativa**: Escolhido pela alta performance (async nativo) e facilidade de manutenção. O FastAPI gera documentação automática (Swagger) e utiliza Pydantic para validação de tipos, o que reduz drasticamente erros de comunicação com o frontend. Comparado ao Flask, o FastAPI é mais moderno e escala melhor para APIs REST.

### 4.2.2. Estratégia de Paginação: Option A (Offset-based)
- **Justificativa**: Como o volume de operadoras é moderado (~4.000 registros), a paginação por Offset é ideal. Ela permite que o usuário saiba o total de páginas e pule para uma página específica na interface, algo que o Cursor-based dificulta. A performance do SQLite para esse volume é excelente mesmo com offsets altos.

### 4.2.3. Cache vs Queries Diretas: Option C (Pré-calcular)
- **Justificativa**: Os dados da ANS são atualizados trimestralmente. Portanto, os resultados da rota `/api/estatisticas` são estáticos durante a vida útil do sistema. No backend, as queries agregam milhões de linhas; por isso, em um cenário real, esses valores seriam calculados uma única vez após a carga dos dados e armazenados ou cacheados em memória para resposta instantânea.

### 4.2.4. Estrutura de Resposta: Option B (Dados + Metadados)
- **Justificativa**: Retornar `{data: [], total: 100, page: 1}` é essencial para o frontend. Sem o metadado `total`, o componente de paginação não saberia quantas páginas exibir, degradando a experiência do usuário.

---

## 🎨 Justificativas e Trade-offs: Frontend

### 4.3.1. Estratégia de Busca/Filtro: Option A (Busca no Servidor)
- **Justificativa**: Embora tenhamos "apenas" 4.000 operadoras, o volume de despesas associadas chega a milhões. Realizar filtros no servidor garante que a aplicação frontend permaneça leve e rápida, carregando apenas o necessário através da API paginada.

### 4.3.2. Gerenciamento de Estado: Option B (Pinia)
- **Justificativa**: Pinia (sucessor do Vuex) foi utilizado para centralizar o estado das operadoras e estatísticas. Isso facilita o compartilhamento de dados entre a Home e a página de Detalhes, além de proporcionar uma arquitetura mais limpa e testável para o crescimento da aplicação.

### 4.3.3. Performance da Tabela: Virtualização vs Paginação
- **Justificativa**: Escolhemos **Paginação Padrão**. Para o usuário final que analisa dados regulatórios, a paginação é mais familiar e permite um controle melhor da navegação do que o "Infinite Scroll", além de ser mais simples de implementar com SEO em mente.

### 4.3.4. Tratamento de Erros e Loading
- **Loading**: Implementado via estados reativos no Pinia, exibindo um *spinner* visual no centro da tabela durante requisições.
- **Erros**: As falhas de API são capturadas pelo bloco `try/catch` do Axios, exibindo mensagens específicas ao usuário caso o servidor esteja offline ou o dado não exista.
- **Análise Crítica**: Optamos por mensagens amigáveis em vez de erros técnicos puros, melhorando a UX e facilitando a identificação de problemas (ex: "Operadora não encontrada").

---

## 📂 Como Executar

### 1. Backend
```bash
cd desafio_04_api_interface/backend
pip install -r requirements.txt
python main.py
```
A API estará disponível em `http://localhost:8000`. Acesse `/docs` para ver o Swagger.

### 2. Frontend
```bash
cd desafio_04_api_interface/frontend
npm install
npm run dev
```
O dashboard estará disponível em `http://localhost:5173`.

---

## 📝 Documentação API
A coleção completa para o Postman está localizada em: `postman/ans_api_collection.json`.
