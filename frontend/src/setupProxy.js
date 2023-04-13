const { createProxyMiddleware } = require('http-proxy-middleware');

const context = [
  '/api',
]

// make the proxy work for all requests
// const context = '/*';

module.exports = function(app) {
  app.use(
    context,
    createProxyMiddleware({
      target: 'http://127.0.0.1:5000',
      changeOrigin: true,
    })
  );
};

// const apiProxy = createProxyMiddleware({
//   target: 'http://localhost:3000',
//   pathFilter: ['/api', '/test'],
// });

// module.exports = {
//   port: 3000,
//   server: {
//     middleware: [
//       apiProxy,
//     ],
//   },
// }