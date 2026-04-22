import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from negocio.services.accident_service import (
    get_accidents,
    get_day_night_breakdown,
    get_hourly_distribution,
    get_top_states,
    get_weekday_distribution,
)
from negocio.services.llm_service import ask_accidents_llm, get_tool_catalog


def _parse_optional_int(value: str | None, field_name: str) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"El parametro '{field_name}' debe ser numerico.") from exc


@require_GET
def health(_request):
    return JsonResponse({"status": "ok", "service": "us-accidents-api"})


@require_GET
def list_accidents(request):
    try:
        limit = _parse_optional_int(request.GET.get("limit"), "limit") or 20
        offset = _parse_optional_int(request.GET.get("offset"), "offset") or 0
        severity = _parse_optional_int(request.GET.get("severity"), "severity")
        state = (request.GET.get("state") or "").strip().upper() or None

        if limit < 1:
            raise ValueError("El parametro 'limit' debe ser mayor o igual a 1.")
        if offset < 0:
            raise ValueError("El parametro 'offset' debe ser mayor o igual a 0.")

        result = get_accidents(limit=limit, offset=offset, state=state, severity=severity)
        return JsonResponse(result.model_dump(mode="json"))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)


@require_GET
def top_states(request):
    try:
        limit = _parse_optional_int(request.GET.get("limit"), "limit") or 10
        if limit < 1:
            raise ValueError("El parametro 'limit' debe ser mayor o igual a 1.")
        result = get_top_states(limit=limit)
        return JsonResponse(result.model_dump(mode="json"))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)


@require_GET
def day_night_breakdown(_request):
    result = get_day_night_breakdown()
    return JsonResponse(result.model_dump(mode="json"))


@require_GET
def hourly_distribution(_request):
    result = get_hourly_distribution()
    return JsonResponse(result.model_dump(mode="json"))


@require_GET
def weekday_distribution(_request):
    result = get_weekday_distribution()
    return JsonResponse(result.model_dump(mode="json"))


@require_GET
def llm_tools(_request):
    return JsonResponse(get_tool_catalog())


@csrf_exempt
def ask_accidents(request):
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido. Usa POST."}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Body JSON invalido."}, status=400)

    question = (payload.get("question") or "").strip()
    if not question:
        return JsonResponse({"error": "El campo 'question' es obligatorio."}, status=400)

    try:
        result = ask_accidents_llm(question)
        return JsonResponse(result)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
