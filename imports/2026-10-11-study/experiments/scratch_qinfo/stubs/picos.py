# stub so toqito imports without picos; only annotations reference picos in the code paths used
class _Anything:
    def __getattr__(self, k): return _Anything()
    def __call__(self, *a, **k): return _Anything()
    def __or__(self, o): return self
    def __ror__(self, o): return self
    def __getitem__(self, k): return self
def __getattr__(name): return _Anything()
