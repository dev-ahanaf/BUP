"""FastAPI application entry point for GridWise Energy Optimization Service."""
import time
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from app.config import settings
from app.dashboard import get_dashboard_html
from app.models.response import HealthResponse, OptimizationResponse
from app.models.request import OptimizationRequest
from app.utils.logging import logger

app = FastAPI(
    title="GridWise Energy Optimization API",
    description="LLM-guided, MILP-optimized smart campus energy dispatch system.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors with clear, structured JSON."""
    logger.warning(f"Request validation error for {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Invalid request payload schema or constraint violation",
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global fallback exception handler."""
    logger.error(f"Unhandled exception during {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred during optimization processing"},
    )


@app.get(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    summary="Interactive Energy Optimization Dashboard",
    description="Serves the web dashboard for scenario testing, health monitoring, and documentation links.",
)
async def dashboard() -> str:
    """Serve the interactive web test bench and system dashboard."""
    return get_dashboard_html()


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Returns service status to verify the server is live and ready.",
)
async def health_check() -> Dict[str, str]:
    """Health check endpoint returning {'status': 'ok'}."""
    return {"status": "ok"}


@app.post(
    "/optimize-energy",
    response_model=OptimizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Optimize 24-hour campus energy dispatch under operator directives",
    description="Interprets natural language operator notes, applies mathematical constraints, solves the MILP dispatch schedule, verifies all physical balances via replay validator, and returns the optimal dispatch plan.",
)
async def optimize_energy(request: OptimizationRequest) -> OptimizationResponse:
    """Optimize energy dispatch endpoint."""
    start_time = time.time()
    logger.info(f"Received optimization request for scenario '{request.scenario_id}' with {len(request.operator_notes)} notes")

    # Lazy import to avoid circular dependencies during initialization
    from app.services.optimization_service import OptimizationService

    service = OptimizationService()
    try:
        response = await service.process_scenario(request)
        elapsed = time.time() - start_time
        logger.info(f"Successfully optimized scenario '{request.scenario_id}' in {elapsed:.3f}s: total_cost={response.total_cost_bdt:.2f} BDT")
        return response
    except ValueError as e:
        logger.error(f"Validation / processing error for '{request.scenario_id}': {str(e)}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing '{request.scenario_id}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Optimization failed: {str(e)}")
