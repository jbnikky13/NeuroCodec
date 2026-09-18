# NeuroCodec Architecture

```
Structured input
      |
      v
Parallel data encoder
      |
      v
Shared latent representation <---- Format specification encoder
      |                                      ^
      v                                      |
Conditional decoder -------------------------+
      |
      v
Target representation
      |
      +----> benchmark metrics
      |
      +----> translation receipt
                    |
                    v
             SHA-256 digest
                    |
                    v
             Arc settlement intent
```

The streaming adapter supplies recent observations for bounded online adaptation. The API exposes the research pipeline without making blockchain state part of the neural model.
