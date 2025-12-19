from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/test/admin-ws", response_class=HTMLResponse)
def admin_ws_test():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>Admin WebSocket Test</title>
</head>
<body>
  <h3>Admin WebSocket</h3>
  <pre id="log"></pre>

  <script>
    const log = msg => {
      document.getElementById("log").innerText += msg + "\\n";
    };

    log("PAGE LOADED");

    const ws = new WebSocket("ws://127.0.0.1:8000/ws/admin");

    ws.onopen = () => log("CONNECTED ✅");
    ws.onmessage = e => log("MESSAGE 🔔: " + e.data);
    ws.onerror = e => log("ERROR ❌");
    ws.onclose = () => log("CLOSED 🔒");
  </script>
</body>
</html>
"""
