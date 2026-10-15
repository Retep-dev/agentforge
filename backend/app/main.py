from fastapi import FastAPI
from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph
from typing import TypedDict

app = FastAPI(title="AgentForge API", version="0.1.0")


class PlanState(TypedDict):
    goal: str
    steps: list[str]


def outline(state: PlanState) -> PlanState:
    goal = state["goal"].strip()
    return {"goal": goal, "steps": [f"Define success criteria for {goal}", f"Build a small prototype for {goal}", f"Evaluate the prototype for {goal}"]}


graph_builder = StateGraph(PlanState)
graph_builder.add_node("outline", outline)
graph_builder.set_entry_point("outline")
graph_builder.add_edge("outline", END)
planner = graph_builder.compile()


class PlanRequest(BaseModel):
    goal: str = Field(min_length=3, max_length=300)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/plan")
def plan(request: PlanRequest) -> PlanState:
    return planner.invoke({"goal": request.goal, "steps": []})
