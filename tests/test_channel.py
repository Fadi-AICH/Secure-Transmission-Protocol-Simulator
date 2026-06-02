from core.channel.error_models import ErrorMode
from core.channel.noisy_channel import NoisyChannel


def test_noisy_channel_seed_is_deterministic() -> None:
    channel_a = NoisyChannel(seed=7)
    channel_b = NoisyChannel(seed=7)
    result_a = channel_a.transmit("10101010", ErrorMode.MULTI, 0.5)
    result_b = channel_b.transmit("10101010", ErrorMode.MULTI, 0.5)
    assert result_a.transmitted_bits == result_b.transmitted_bits
    assert result_a.modified_indexes == result_b.modified_indexes


def test_noisy_channel_can_inject_single_error() -> None:
    channel = NoisyChannel(seed=1)
    result = channel.transmit("10101010", ErrorMode.SINGLE, 1.0)
    assert len(result.modified_indexes) == 1
