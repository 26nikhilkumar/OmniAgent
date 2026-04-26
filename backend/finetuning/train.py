from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.finetuning.dataset import build_synthetic_tool_calling_dataset


def export_jsonl(path: str = "data/finetune/train.jsonl") -> str:
    Path("data/finetune").mkdir(parents=True, exist_ok=True)
    rows = build_synthetic_tool_calling_dataset()
    out = Path(path)
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(
                (
                    '{"instruction": "' + row.instruction + '", '
                    '"input": "' + row.input_text + '", '
                    '"output": "' + row.output_text.replace('"', '\\"') + '"}\n'
                )
            )
    return str(out)


if __name__ == "__main__":
    print(export_jsonl())
