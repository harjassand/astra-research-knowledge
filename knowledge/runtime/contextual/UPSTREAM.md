# Contextual retrieval encoder

BAAI/bge-small-en-v1.5 at5c38ec7c405ec4b44b94cc5a9bb96e735b38267a. The pinned publisher model card declaresMIT and specifies CLS pooling, unit normalization and the general query instruction. Passages do not receive that query instruction.

Model card: https://huggingface.co/BAAI/bge-small-en-v1.5/blob/5c38ec7c405ec4b44b94cc5a9bb96e735b38267a/README.md

LICENSE.txt is the unchanged official FlagEmbedding MIT implementation license from https://raw.githubusercontent.com/FlagOpen/FlagEmbedding/897baa67c0ffddbfccf4e6776ff55310d67809d4/LICENSE. The model license declaration is separately in PUBLISHER_MODEL_CARD.md. BAAI/FlagEmbedding attribution is retained; no additional rights or scientific endorsement are claimed.

The133093490-byte publisher ONNX source has SHA256828e1496d7fabb79cfa4dcd84fa38625c0d3d21da474a00f08db0f559940cf35. model.onnx stores FLOAT initializers as float16 with explicit casts restoring FLOAT before every original consumer; graph computations remain float32. There is no fitted calibration or query-specific optimization. Rebuild instructions and pinned conversion versions are in CONVERSION.json. This storage conversion fits an ordinary public Git blob. It is a retrieval encoder, not a research-generating language model.
