import json
import os
from typing import Any

from openai import OpenAI

from negocio.services.accident_service import (
    get_day_night_breakdown,
    get_hourly_distribution,
    get_top_states,
    get_weekday_distribution,
)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "name": "get_top_states",
        "description": "Returns the states with most accidents. Mirrors GET /api/analytics/top-states/.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 50,
                    "description": "How many top states to return.",
                }
            },
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_day_night_breakdown",
        "description": "Returns accident counts for Day vs Night. Mirrors GET /api/analytics/day-night/.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_hourly_distribution",
        "description": "Returns accident counts by hour of day (0-23). Mirrors GET /api/analytics/hourly/.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_weekday_distribution",
        "description": "Returns accident counts by ISO weekday. Mirrors GET /api/analytics/weekday/.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
]


SYSTEM_PROMPT = (
    "You are an analytics assistant for US accidents. "
    "Use tools to answer with evidence from data. "
    "If user asks about state/day-night/hour/weekday patterns, call the matching tool(s) before answering. "
    "When possible, summarize the top finding with exact counts from tool outputs."
)


def _execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "get_top_states":
        limit = int(arguments.get("limit", 10))
        return get_top_states(limit=limit).model_dump(mode="json")
    if name == "get_day_night_breakdown":
        return get_day_night_breakdown().model_dump(mode="json")
    if name == "get_hourly_distribution":
        return get_hourly_distribution().model_dump(mode="json")
    if name == "get_weekday_distribution":
        return get_weekday_distribution().model_dump(mode="json")
    raise ValueError(f"Unsupported tool: {name}")


def ask_accidents_llm(question: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no esta configurada en variables de entorno.")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        tools=TOOL_DEFINITIONS,
    )

    tool_calls_trace: list[dict[str, Any]] = []

    for _ in range(6):
        function_calls = [item for item in response.output if item.type == "function_call"]
        if not function_calls:
            return {
                "answer": response.output_text,
                "model": OPENAI_MODEL,
                "tool_calls": tool_calls_trace,
            }

        function_outputs = []
        for call in function_calls:
            raw_args = call.arguments or "{}"
            args = json.loads(raw_args)
            result = _execute_tool(call.name, args)
            tool_calls_trace.append({"tool": call.name, "arguments": args, "result": result})
            function_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result),
                }
            )

        response = client.responses.create(
            model=OPENAI_MODEL,
            previous_response_id=response.id,
            input=function_outputs,
            tools=TOOL_DEFINITIONS,
        )

    raise ValueError("El modelo no finalizo la respuesta despues de varios tool calls.")


def get_tool_catalog() -> dict[str, Any]:
    return {
        "tools": TOOL_DEFINITIONS,
        "endpoint_mapping": {
            "get_top_states": "/api/analytics/top-states/?limit=10",
            "get_day_night_breakdown": "/api/analytics/day-night/",
            "get_hourly_distribution": "/api/analytics/hourly/",
            "get_weekday_distribution": "/api/analytics/weekday/",
        },
    }
