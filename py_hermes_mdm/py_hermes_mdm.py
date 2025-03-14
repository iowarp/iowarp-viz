
from py_hermes import Hermes, TRANSPARENT_HERMES, IoType

class MetadataSnapshot:
    """
    Three tables will be collected:
    1. Blob Info:
      
    2. Target Info
    3. Tag Info
    """
    def __init__(self):
        TRANSPARENT_HERMES()
        self.hermes = Hermes()
        self.blob_info = []
        self.target_info = []
        self.tag_info = []
        self.io_stats = []
        self.tid_to_tgt = {}
        self.tag_to_blob = {}
        self.last_access = 0

    def collect_target_md(self, filter, max_count):
        targets = self.hermes.PollTargetMetadata(filter, max_count)
        self.target_info = []
        for target in targets:
            target_info = {
                'name': None,
                'id':  self.unique(target.tgt_id),
                'node_id': int(target.node_id),
                'rem_cap': target.rem_cap,
                'max_cap': target.max_cap,
                'bandwidth': target.bandwidth,
                'latency': target.latency,
                'score': target.score,
            }
            self.target_info.append(target_info)
            self.tid_to_tgt[target_info['id']] = target_info
        self.target_info.sort(reverse=True, key=lambda x: x['bandwidth'])
        for i, target in enumerate(self.target_info):
            target['name'] = f'Tier {i}'
    
    def collect_blob_md(self, filter, max_count):
        blobs = self.hermes.PollBlobMetadata(filter, max_count)
        self.blob_info = []
        for blob in blobs:
            blob_info = {
                'name': str(blob.get_name()),
                'id': self.unique(blob.blob_id),
                'mdm_node': int(blob.blob_id.node_id),
                'tag_id': self.unique(blob.tag_id),
                'score': float(blob.score),
                'access_frequency': 0,
                'buffer_info': []
            }
            for buf in blob.buffers:
                buf_info = {
                    'target_id': self.unique(buf.tid),
                    'node_id': 0,
                    'size': int(buf.size)
                }
                buf_info['node_id'] = self.tid_to_tgt[buf_info['target_id']]['node_id']
                blob_info['buffer_info'].append(buf_info)
            self.blob_info.append(blob_info)
            if blob_info['tag_id'] not in self.tag_to_blob:
                self.tag_to_blob[blob_info['tag_id']] = []
            self.tag_to_blob[blob_info['tag_id']].append(blob_info['id'])

    def collect_tag_md(self, filter, max_count):
        tags = self.hermes.PollTagMetadata(filter, max_count)
        for tag in tags:
            tag_info = {
                'id': self.unique(tag.tag_id),
                'mdm_node': int(tag.tag_id.node_id),
                'name': str(tag.get_name()),
                # 'blobs': [self.unique(blob.blob_id) for blob in tag.blobs]
                'blobs': []
            }
            if tag_info['id'] in self.tag_to_blob:
                tag_info['blobs'] = self.tag_to_blob[tag_info['id']]
            self.tag_info.append(tag_info)

    def collect_access_pattern(self):
        self.io_stats = []
        io_stats = self.hermes.PollAccessPattern(self.last_access)
        for io_stat in io_stats: 
            self.io_stats.append({
                'type': self.get_io_type(io_stat.type),
                'blob_id': self.unique(io_stat.blob_id),
                'tag_id': self.unique(io_stat.tag_id),
                'blob_size': io_stat.blob_size,
                'id': int(io_stat.id),
                'blob_size': int(io_stat.blob_size),
            })
        if len(io_stats) > 0:
            self.last_access = int(io_stats[-1].id)

    @staticmethod
    def unique(id):
        return f'{id.node_id}.{id.unique}'

    @staticmethod
    def get_io_type(io_type):
        if io_type == IoType.kRead:
            return 'read'
        elif io_type == IoType.kWrite:
            return 'write'
        else:
            return 'none'
        
