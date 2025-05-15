from typing import Any, Callable, Dict, Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

class Resource:
    def __init__(self, path: str, handler: Callable):
        self.path = path
        self.handler = handler

class Tool:
    def __init__(self, name: str, handler: Callable):
        self.name = name
        self.handler = handler

class MCP:
    def __init__(self):
        self.app = FastAPI()
        self.resources: Dict[str, Resource] = {}
        self.tools: Dict[str, Tool] = {}
        self._setup_routes()

    def resource(self, path: str):
        def decorator(handler: Callable):
            self.resources[path] = Resource(path, handler)
            return handler
        return decorator

    def tool(self, name: Optional[str] = None):
        def decorator(handler: Callable):
            tool_name = name or handler.__name__
            self.tools[tool_name] = Tool(tool_name, handler)
            return handler
        return decorator

    def _setup_routes(self):
        @self.app.post("/mcp/resource/{path:path}")
        async def handle_resource(path: str, request: Request):
            try:
                data = await request.json()
                resource = self.resources.get(path)
                if not resource:
                    return JSONResponse(
                        status_code=404,
                        content={"error": f"Resource not found: {path}"}
                    )
                result = await resource.handler(**data)
                return JSONResponse(content=result)
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.post("/mcp/tool/{name}")
        async def handle_tool(name: str, request: Request):
            try:
                data = await request.json()
                tool = self.tools.get(name)
                if not tool:
                    return JSONResponse(
                        status_code=404,
                        content={"error": f"Tool not found: {name}"}
                    )
                result = await tool.handler(**data)
                return JSONResponse(content=result)
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

    def run(self, host: str = "localhost", port: int = 8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port) 