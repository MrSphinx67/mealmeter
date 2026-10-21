"""Korak 4: MCP poslužitelj kroz MCP klijent u procesu (mcp.Client nad MCPServer)."""

import asyncio
import json

import pytest
from mcp import Client

from mealmeter import server as srv

TOOLS = {"find_products", "get_prices", "plan_basket", "list_stores", "convert_units", "list_staples"}


def _run(coro):
    return asyncio.run(coro)


async def _tools():
    async with Client(srv.create_server()) as c:
        return (await c.list_tools()).tools, c.instructions


def test_descriptions_bilingual():
    tools, instructions = _run(_tools())
    assert {t.name for t in tools} == TOOLS
    for t in tools:
        d = t.description
        # hrvatski / engleski: što radi (prvi redak "hr / en"), kada, parametri, primjer
        head = d.split("Kada / when")[0].strip().splitlines()  # opis: "hr / en" ili redak hr pa redak en
        assert len(head) >= 2 or " / " in head[0], t.name
        assert "Kada / when" in d and "Primjer / example" in d, t.name
        assert t.name == "list_staples" or "Parametri / parameters" in d, t.name
        assert t.annotations.read_only_hint
    for word in ("convert_units", "already_have", "store", "date_hr", "stale_days", "total_to_buy", "total_used",
                 "warnings", "ambiguity", "assumed_form", "match_quality", "alternatives", "price_overrides",
                 "zaliha", "stock", "izmišljaj"):
        assert word in instructions, word
