from pydantic import BaseModel


class GenerateRequest(BaseModel):
    model: str | None = None
    prompt: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str | None = None


class ModelInfoRequest(BaseModel):
    model: str
    verbose: bool = False


class EmbedRequest(BaseModel):
    input: str | list[str]
    model: str | None = None


class SamplingOptions(BaseModel):
    temperature: float | None = None
    seed: int | None = None
    top_k: int | None = None
    top_p: float | None = None
    num_predict: int | None = None
    system: str | None = None


class GenerateWithOptionsRequest(BaseModel):
    prompt: str
    model: str | None = None
    options: SamplingOptions | None = None