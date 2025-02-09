# Desafio de Análise de Conversa com OpenAI 🚀

Olá, pessoal! Tudo bem? :)

Obrigada pela oportunidade de participar deste processo seletivo! Este projeto foi desenvolvido com o objetivo de demonstrar habilidades técnicas, criatividade na resolução de problemas e integração de tecnologias modernas como a OpenAI API e PostgreSQL.

## O que foi implementado de diferente? 💡

Durante o desenvolvimento do projeto, realizei algumas melhorias e customizações além do esperado:

### Novas colunas na tabela `analysis`
Adicionei as seguintes colunas para enriquecer a análise e armazenar informações detalhadas das interações:
- `effort_score` (Pontuação de esforço)
- `negative_points` (Pontos negativos destacados pela análise)
- `positive_points` (Pontos positivos destacados pela análise)
- `resolution_status` (Status de resolução)
- `tone` (Tom da conversa)

Essas alterações tornam a análise mais completa, fornecendo insights valiosos sobre as interações.

### Criação do Prompt para a OpenAI

O prompt foi cuidadosamente elaborado para solicitar uma análise detalhada à API da OpenAI. Ele inclui:

- **Tom da conversa:** Se a interação foi cordial, amigável, formal, etc.
- **Resumo da interação:** Uma descrição geral do que ocorreu na conversa.
- **Sugestões de melhoria:** Pontos de melhoria na interação.
- **Pontos positivos:** Destaques positivos do atendimento.
- **Pontos negativos:** Destaques negativos do atendimento.
- **Status de resolução:** Informação se o problema foi resolvido ou não.
- **Nível de satisfação:** Uma pontuação de 1 a 10 sobre a experiência do cliente.
- **Esforço do cliente:** Uma pontuação para avaliar o esforço necessário do cliente durante a interação.

Isso garante que a análise seja precisa, útil e bem estruturada.

### Workflow otimizado
Foi criado um fluxo que busca mensagens de uma sessão, envia para a OpenAI para análise e, em seguida, persiste os resultados no banco de dados PostgreSQL.

## Como rodar o projeto localmente?

### Pré-requisitos
Certifique-se de ter instalado:
- **Docker** e **Docker Compose**
- **Python 3.10+**

### Passos para rodar o projeto

1. Suba os serviços do Docker (banco de dados e aplicação):
   ```bash
   docker-compose up --build

2. Acesse a aplicação em [http://localhost:8000](http://localhost:8000)🌐.

3. Para testar a API, utilize ferramentas como **Postman** ou **cURL**. Por exemplo:

   - **Rota:** `POST /analyze/{session_id}`
   - **Corpo da requisição:**
     ```json
     {
       "session_id": 3
     }
     ```

   📊 Os resultados da análise serão salvos no banco de dados PostgreSQL. Você pode visualizar os dados utilizando ferramentas como **pgAdmin** ou qualquer cliente SQL.

---

## Agradecimentos 🙏

Mais uma vez, agradeço pela oportunidade de participar do desafio! Espero passar para a próxima etapa.

Atenciosamente,

Isadora Estanislau

