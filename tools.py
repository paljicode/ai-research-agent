import os
import ast
import operator
from typing import Dict, Any, Union
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# --- SAFE CALCULATOR TOOL ---

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval_expr(node: ast.AST) -> Union[int, float]:
    """Safely evaluate a mathematical AST node without using unrestricted eval()."""
    if isinstance(node, ast.Expression):
        return safe_eval_expr(node.body)
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Invalid constant: {node.value}")
    elif isinstance(node, ast.BinOp):
        left = safe_eval_expr(node.left)
        right = safe_eval_expr(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            if op_type == ast.Div and right == 0:
                raise ZeroDivisionError("Division by zero is undefined.")
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval_expr(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    else:
        raise ValueError(f"Unsupported syntax expression: {type(node).__name__}")


def calculator_tool(expression: str) -> Dict[str, Any]:
    """
    Safely calculates mathematical expressions.
    Handles formulas like ((150 - 100) / 100) * 100.
    """
    try:
        # Clean input expression
        cleaned_expr = expression.replace("%", "").strip()
        parsed_ast = ast.parse(cleaned_expr, mode='eval')
        result = safe_eval_expr(parsed_ast)
        return {
            "status": "success",
            "expression": expression,
            "result": round(result, 4),
            "error": None
        }
    except ZeroDivisionError:
        return {
            "status": "error",
            "expression": expression,
            "result": None,
            "error": "Standard percentage increase is undefined when the initial value is zero (division by zero)."
        }
    except Exception as e:
        return {
            "status": "error",
            "expression": expression,
            "result": None,
            "error": f"Invalid expression or evaluation error: {str(e)}"
        }


# --- SEARCH TOOL ---

def search_tool(search_query: str) -> Dict[str, Any]:
    """
    Performs web search using Tavily API and returns structured sources.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "query": search_query,
            "results": [],
            "error": "TAVILY_API_KEY is missing from environment variables."
        }

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=search_query, max_results=3)

        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title", "No Title"),
                "snippet": r.get("content", ""),
                "url": r.get("url", "")
            })

        return {
            "status": "success",
            "query": search_query,
            "results": results,
            "error": None
        }
    except Exception as e:
        return {
            "status": "error",
            "query": search_query,
            "results": [],
            "error": f"Search API error: {str(e)}"
        }