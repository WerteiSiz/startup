from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import httpx
import logging
from typing import Optional
from jose import JWTError, jwt
import os
from fastapi.middleware.cors import CORSMiddleware
from .rate_limiting import rate_limit_middleware

logger = logging.getLogger(__name__)

app = FastAPI(title="API Gateway")

# Вместо Jinja2Templates, используем прямое чтение файлов
def render_template(template_name: str):
    template_path = os.path.join(os.path.dirname(__file__), "templates", template_name)
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Middleware
@app.middleware("http")
async def add_rate_limiting(request: Request, call_next):
    return await rate_limit_middleware(request, call_next)

# ================== MIDDLEWARE ==================
@app.middleware("http")
async def auth_middleware(request: Request, call_next): 
    if request.method == "OPTIONS":
        return await call_next(request)
    
    public_paths = [
        '/', '/api/v1/auth/login', '/register', '/api/v1/health',
        '/api/v1/login',
        '/api/v1/auth/register', '/api/v1/auth/send_code'
    ]


    if request.url.path in public_paths:
        return await call_next(request)
    
    token = request.cookies.get("access_token")
    
    if not token:
        if request.url.path.startswith('/api/'):
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        else:
            return RedirectResponse(url="/login")
        
    try:
        payload = jwt.decode(
            token, 
            os.getenv('JWT_SECRET_KEY'), 
            algorithms=[os.getenv('JWT_ALGORITHM')]
        )
        logger.info(f"✅ Valid JWT for user: {payload.get('sub')}")
    except jwt.ExpiredSignatureError:
        if request.url.path.startswith('/api/'):
            return JSONResponse(status_code=401, content={"error": "Token expired"})
        else:
            return RedirectResponse(url="/login")
    except jwt.JWTError as e:
        logger.error(f"❌ JWT validation error: {e}")
        if request.url.path.startswith('/api/'):
            return JSONResponse(status_code=401, content={"error": "Invalid token"})
        else:
            return RedirectResponse(url="/login")
    
    request.state.user = payload
    response = await call_next(request)
    return response

# ================== HTML РОУТЫ ==================
@app.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    html_content = render_template("login.html")
    return HTMLResponse(content=html_content)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    html_content = render_template("login.html")
    return HTMLResponse(content=html_content)

@app.get("/register", response_class=HTMLResponse)  
async def register_page(request: Request):
    html_content = render_template("register.html")
    return HTMLResponse(content=html_content)

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    html_content = render_template("profile.html")
    return HTMLResponse(content=html_content)

@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    html_content = render_template("orders.html")
    return HTMLResponse(content=html_content)

# ================== ПРОКСИРОВАНИЕ ==================
@app.api_route("/api/v1/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_users(request: Request, path: str):
    return await proxy_request(request, path)

@app.api_route("/api/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_users(request: Request, path: str):
    return await proxy_request(request, path)

async def proxy_request(request: Request, path: str):
    target_url = f"http://service_users:8000/api/v1/{path}"
    headers = {
        key: value for key, value in request.headers.items()
        if key.lower() not in ['host', 'content-length']
    }
    
    if hasattr(request.state, 'user'):
        user_data = request.state.user
        headers["X-User-ID"] = str(user_data.get("user_id", ""))
        headers["X-User-Email"] = str(user_data.get("sub", ""))
        headers["X-User-Roles"] = str(",".join(user_data.get("roles", [])))
    
    body = await request.body()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            return JSONResponse(
                content=response.json() if response.content else {},
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Service unavailable")
    except Exception as e:
        logger.error(f"Error proxying to: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal gateway error")

# ================== HEALTH CHECK ==================
@app.get("/health")
async def health():
    return {"status": "API Gateway is healthy"}

@app.get("/api/health")
async def api_health():
    return {"status": "API Gateway API is healthy"}