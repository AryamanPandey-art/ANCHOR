"""Troubleshoot router."""

from fastapi import APIRouter, Depends
from backend.models.request import TroubleshootRequest
from backend.pipeline.orchestrator import PipelineOrchestrator
from student_kit.schema import ContextDeeplinkResponse

router = APIRouter()


def get_orchestrator() -> PipelineOrchestrator:
    return PipelineOrchestrator()


@router.post(
    "/v1/troubleshoot",
    response_model=ContextDeeplinkResponse,
    tags=["Troubleshoot"]
)
def troubleshoot(
    request: TroubleshootRequest,
    orchestrator: PipelineOrchestrator = Depends(get_orchestrator)
) -> ContextDeeplinkResponse:
    """Guided troubleshooting endpoint for Smart Guided Troubleshooting Engine."""
    return orchestrator.process(request)
