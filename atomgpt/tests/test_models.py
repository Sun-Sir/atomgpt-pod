import torch
import transformers
from atomgpt.models.causal import AtomGPTPredictorLMhead


class DummyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # minimal config with hidden_size attribute
        self.config = type("config", (), {"hidden_size": 4})()

    def resize_token_embeddings(self, size: int):
        pass

    def forward(self, input_ids, decoder_input_ids=None):
        return input_ids


def test_causal_forward_uses_model_name(monkeypatch):
    """Ensure forward uses the instance's model name attribute."""
    monkeypatch.setattr(
        transformers.T5ForConditionalGeneration,
        "from_pretrained",
        lambda *args, **kwargs: DummyModel(),
    )

    class DummyTokenizer:
        def __len__(self):
            return 10

    model = AtomGPTPredictorLMhead(model_name="t5", tokenizer=DummyTokenizer())
    inp = torch.zeros((1, 1), dtype=torch.long)
    out = model.forward(inp)
    assert out.shape == inp.shape
