from dataclasses import dataclass


@dataclass
class FinetuneExample:
    instruction: str
    input_text: str
    output_text: str


def build_synthetic_tool_calling_dataset() -> list[FinetuneExample]:
    return [
        FinetuneExample(
            instruction="Call search tool",
            input_text="Find latest papers on hybrid RAG",
            output_text='{"tool":"search_web","arguments":{"query":"latest papers on hybrid RAG"}}',
        ),
        FinetuneExample(
            instruction="Call scheduling tool",
            input_text="Remind me in two weeks to review findings",
            output_text='{"tool":"schedule_reminder","arguments":{"event":"review findings","days_from_now":14}}',
        ),
    ]
