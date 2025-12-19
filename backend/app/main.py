from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import time

from app.core.config import APP_NAME

# =========================
# API ROUTERS
# =========================
from app.api import chat
from app.api import agent
from app.api import override
from app.api import dashboard
from app.api import dashboard_ticket_detail
from app.api import dashboard_metrics
from app.api import admin_actions
from app.api import ws_admin
from app.api import test_ws_page

# =========================
# SERVICES
# =========================
from app.services.sla_service import SLAService

# =========================
# APP INITIALIZATION
# =========================

app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    description="AI Customer Support Backend"
)

# =========================
# CORS CONFIG
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTER REGISTRATION
# =========================

app.include_router(chat.router, prefix="/api")
app.include_router(agent.router, prefix="/api/agent")
app.include_router(override.router, prefix="/api")

app.include_router(dashboard.router, prefix="/api/dashboard")
app.include_router(dashboard_ticket_detail.router, prefix="/api/dashboard")
app.include_router(dashboard_metrics.router, prefix="/api/dashboard")

app.include_router(admin_actions.router, prefix="/api/admin")

app.include_router(test_ws_page.router)
app.include_router(ws_admin.router)

# =========================
# SLA BACKGROUND WORKER
# =========================

def sla_background_worker():
    time.sleep(5)  # allow app to fully boot
    while True:
        try:
            SLAService.run_sla_check()
        except Exception as e:
            print(f"[SLA ERROR] {e}")
        time.sleep(60)


@app.on_event("startup")
def start_background_services():
    if not hasattr(app.state, "sla_started"):
        app.state.sla_started = True
        thread = threading.Thread(
            target=sla_background_worker,
            daemon=True
        )
        thread.start()

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "service": "AI Support Backend"
    }

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "AI Support Backend Running",
        "health": "OK"
    }
