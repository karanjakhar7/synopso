import os
import re

from litellm import Router
from litellm.exceptions import RateLimitError
from tenacity import retry, stop_after_attempt
from tenacity.wait import wait_base

from ..models import Paper
from ..templates.summarize_paper import summarize_system_message, summarize_user_message

MODEL = os.getenv("MODEL", "openai/gpt-4o-mini")
_NUM_RETRIES = int(os.getenv("LLM_NUM_RETRIES", "3"))
_RPM = int(os.getenv("LLM_RPM", "0"))
_TPM = int(os.getenv("LLM_TPM", "0"))

_litellm_params: dict = {"model": MODEL}
if _RPM:
    _litellm_params["rpm"] = _RPM
if _TPM:
    _litellm_params["tpm"] = _TPM

_router = Router(
    model_list=[{"model_name": MODEL, "litellm_params": _litellm_params}],
)

_RETRY_DELAY_RE = re.compile(r"retry in (\d+(?:\.\d+)?)s", re.IGNORECASE)


class _SmartWait(wait_base):
    """Honour the provider's retry-after for rate limits; exponential backoff otherwise."""

    def __call__(self, retry_state) -> float:
        exc = retry_state.outcome.exception()
        if isinstance(exc, RateLimitError):
            m = _RETRY_DELAY_RE.search(str(exc)) # tries to find the retry delay in the error message
            if m:
                return float(m.group(1)) + 2
            return 60.0
        return min(2 ** retry_state.attempt_number, 60.0)


@retry(
    stop=stop_after_attempt(_NUM_RETRIES),
    wait=_SmartWait(),
    reraise=True,
)
async def summarize_paper_with_ai(paper: Paper) -> str:
    completion = await _router.acompletion(
        model=MODEL,
        messages=[
            {"role": "system", "content": summarize_system_message},
            {
                "role": "user",
                "content": summarize_user_message.format(
                    title=paper.title,
                    authors=paper.authors,
                    text=paper.text,
                ),
            },
        ],
    )
    return completion.choices[0].message.content
