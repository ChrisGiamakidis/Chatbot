# Rasa Webchat 1.0.1

Source: https://cdn.jsdelivr.net/npm/rasa-webchat@1.0.1/lib/index.js

The vendored bundle contains one change: the Socket.IO adapter accepts its
fourth argument (protocolOptions) and forwards those options to socket.io-client,
while preserving socketPath. Upstream 1.0.1 only forwards the path.

This allows index.html to set the ngrok-skip-browser-warning request header for
HTTP polling. Browser WebSocket connections cannot set custom headers.

Upstream project and Apache-2.0 license:
https://github.com/botfront/rasa-webchat
