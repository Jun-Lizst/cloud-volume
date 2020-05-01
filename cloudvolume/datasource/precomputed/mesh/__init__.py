import os

from .metadata import PrecomputedMeshMetadata
from .unsharded import UnshardedLegacyPrecomputedMeshSource


from ..metadata import PrecomputedMetadata
from ....cacheservice import CacheService
from ....exceptions import UnsupportedFormatError
from ....lib import red
from ....paths import strict_extract
from ....cloudvolume import SharedConfiguration

class PrecomputedMeshSource(object):
  def __new__(cls, meta, cache, config, readonly=False):
    mesh_meta = PrecomputedMeshMetadata(meta, cache)

    if mesh_meta.is_sharded():
      raise UnsupportedFormatError(red("This mesh volume is sharded. Mesh shard support is coming but is not available yet."))
      # return ShardedLegacyPrecomputedMeshSource(mesh_meta, cache, config, readonly) 

    return UnshardedLegacyPrecomputedMeshSource(mesh_meta, cache, config, readonly)

  @classmethod
  def from_cloudpath(cls, cloudpath, cache=False, progress=False):
    config = SharedConfiguration(
      cdn_cache=False,
      compress=True,
      compress_level=None,
      green=False,
      mip=0,
      parallel=1,
      progress=progress,
    )

    cache = CacheService(
      cloudpath=(cache if type(cache) == str else cloudpath),
      enabled=bool(cache),
      config=config,
      compress=True,
    )

    cloudpath, mesh_dir = os.path.split(cloudpath)
    meta = PrecomputedMetadata(cloudpath, cache, info={ 'mesh': mesh_dir })

    return PrecomputedMeshSource(meta, cache, config)