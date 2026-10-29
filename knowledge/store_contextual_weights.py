"""Reproduce the published encoder's weight-storage conversion, offline.

Supply the pinned original ONNX artifact and a NEW output path. This tool does
not download models, update the live index or execute scientific source code.
Conversion dependencies: onnx==1.18.0, numpy==2.5.4, protobuf==6.31.1.
"""
import argparse
import hashlib
from pathlib import Path


def main():
    import onnx
    import numpy as np
    from onnx import helper, numpy_helper, TensorProto
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.source.resolve() == args.output.resolve():
        parser.error("Use a new output path; preserve original bytes")
    if hashlib.sha256(args.source.read_bytes()).hexdigest() != "828e1496d7fabb79cfa4dcd84fa38625c0d3d21da474a00f08db0f559940cf35":
        parser.error("Original publisher artifact differs from the pinned source")
    model = onnx.load(str(args.source))
    casts = []
    for tensor in model.graph.initializer:
        if tensor.data_type != TensorProto.FLOAT:
            continue
        name = tensor.name
        stored = name + "__stored_fp16"
        value = numpy_helper.to_array(tensor).astype(np.float16)
        tensor.CopyFrom(numpy_helper.from_array(value, name=stored))
        casts.append(helper.make_node("Cast", [stored], [name], to=TensorProto.FLOAT,
                                      name=stored + "__restore_float32"))
    nodes = list(model.graph.node)
    del model.graph.node[:]
    model.graph.node.extend(casts + nodes)
    onnx.checker.check_model(model)
    raw = model.SerializeToString()
    if hashlib.sha256(raw).hexdigest() != "c3c01b55da19df77b38b8c26f61ebf1895d4ba7bcd15c73f62c39768ea569ca0":
        raise ValueError("Conversion output differs; inspect pinned tool versions before publishing")
    with args.output.open("xb") as stream:
        stream.write(raw)
    print("Pinned contextual weight-storage artifact reproduced exactly.")


if __name__ == "__main__":
    main()
