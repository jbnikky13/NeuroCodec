from __future__ import annotations
from .robustness import check_spec,aggregate

def adversarial_specs():
    return [
      {"name":"unseen-unicode","field_separator":"§","key_value":"⇒","strings":"plain","numbers":"plain"},
      {"name":"multi-char","field_separator":"<F>","key_value":"<K>","strings":"quoted","numbers":"native"},
      {"name":"same-delimiter","field_separator":"|","key_value":"|","strings":"plain","numbers":"plain"},
      {"name":"empty-separator","field_separator":"","key_value":"=","strings":"plain","numbers":"plain"},
      {"name":"empty-key-value","field_separator":"~","key_value":"","strings":"plain","numbers":"plain"},
      {"name":"collision","field_separator":"~","key_value":"=>","strings":"plain","numbers":"plain"},
    ]

def run_adversarial_suite():
    results=[check_spec(s) for s in adversarial_specs()]
    return results,aggregate(results)
