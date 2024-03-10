import argparse
import os
import utils

from mixtral import FiddlerMixtral


def test_generate(args, text):
    model = FiddlerMixtral(args)
    prefill_times = []
    decode_times = []
    hit_rates = []
    batch_sizes = list(range(1, args.batch_size + 1))
    for i in range(1, args.batch_size + 1):
        texts = text * i
        prefill_time, decode_time, hit_rate = model.generate(
            texts, output_token=args.n_token
        )
        prefill_times.append(prefill_time)
        decode_times.append(decode_time)
        hit_rates.append(hit_rate)
        print(
            f"prefill_time: {prefill_time}, decode_time: {decode_time}, hit_rate: {hit_rate}"
        )
    utils.plot(
        batch_sizes,
        prefill_times,
        "beam-prefill_time-batch_size",
        "prefill_time(s)",
        "batch_size",
    )
    utils.plot(
        batch_sizes,
        decode_times,
        "beam-decode_time-batch_size",
        "decode_time(s)",
        "batch_size",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    parser.add_argument(
        "--model",
        type=str,
        default="mistralai/Mixtral-8x7B-v0.1",
        help="Model path. default `mistralai/Mixtral-8x7B-v0.1`.",
    )
    parser.add_argument(
        "--cpu-offload",
        type=int,
        default=1,
        choices=[0, 1],
        help="0: exeute at GPU (baseline), 1: offload to CPU.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="University of Washington is",
        help="Input text to generate.",
    )
    parser.add_argument(
        "--n-token",
        type=int,
        default=20,
        help="Number of tokens to generate.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="Maximum batch size for inference.",
    )
    parser.add_argument("--beam_num", type=int, default=1, help="Beam search number.")

    args = parser.parse_args()

    # model = FiddlerMixtral(args)
    text = ["University of Washington is"]
    test_generate(args, text)
    # prefill_time, decode_time, hit_rate = model.generate(
    #     [args.input] * args.batch_size, output_token=args.n_token
    # )
    # print(
    #     f"prefill_time: {prefill_time}, decode_time: {decode_time}, hit_rate: {hit_rate}"
    # )
