import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.schemas import ResearchDimensions

load_dotenv()


def get_llm():
    return ChatGoogleGenerativeAI(
        #model="gemini-2.5-flash",
        model="gemini-3.6-flash",
        temperature=0,
        max_retries=2,
    )


def generate_research_dimensions(topic: str) -> ResearchDimensions:
    llm = get_llm().with_structured_output(ResearchDimensions)

    prompt = f"""
You are designing a research analysis framework.

Research topic:
{topic}

Identify EXACTLY 10 important dimensions that should be compared
across multiple independent sources researching this topic.

Rules:
- Return exactly 10 dimensions.
- Each dimension must be meaningfully relevant to the topic.
- Prefer dimensions that can contain factual claims or evidence.
- Choose dimensions where sources may agree, disagree, or provide unique information.
- Dimensions should be distinct from each other.
- Do not invent claims.
- Do not summarize any source.
- Return only the structured output requested.

These dimensions will later be used as a fixed comparison framework.
Every source will be evaluated against exactly these same 10 dimensions.
"""

    return llm.invoke(prompt)