import http, { IncomingMessage, ServerResponse } from 'http';

/**
 * Porta em que o servidor será iniciado.
 * 
 * @constant {number} PORT - Porta do servidor (padrão: 3000 ou configurada via env).
 */
const PORT: number = Number(process.env.PORT) || 3000;

/**
 * Função que lida com as requisições HTTP recebidas pelo servidor.
 * 
 * @param {IncomingMessage} req - A requisição HTTP recebida.
 * @param {ServerResponse} res - A resposta HTTP que será enviada.
 * @returns {void} Não retorna nada, apenas responde a requisição.
 */
const requestHandler = (req: IncomingMessage, res: ServerResponse): void => {
  // Define o cabeçalho HTTP para JSON
  res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });

  // Informações que serão enviadas como resposta
  const response = {
    message: 'Servidor Bob está no ar!',
    timestamp: new Date().toISOString(),
    serverName: 'Servidor Bob',
    environment: process.env.NODE_ENV || 'development',
    requestInfo: {
      method: req.method,
      url: req.url,
      headers: req.headers,
    },
    tips: [
      "Seja curioso!",
      "Mantenha seu código limpo.",
      "Testes são seus amigos.",
      "Automatize tudo que for possível!",
    ],
  };

  // Envia o JSON como resposta
  res.end(JSON.stringify(response, null, 2)); // O `null, 2` formata o JSON para facilitar leitura.
};

/**
 * Criação do servidor HTTP.
 * 
 * @constant {http.Server} server - Servidor HTTP que escuta na porta especificada.
 */
const server = http.createServer(requestHandler);

/**
 * Inicia o servidor e escuta na porta configurada.
 * Exibe um log indicando que o servidor está rodando.
 */
server.listen(PORT, () => {
  console.log(`✅ Server is running on port ${PORT}`);
});
