class MetadataSnapshot:
    """
    Three tables will be collected:
    1. Blob Info:
      
    2. Target Info
    3. Tag Info
    """
    def __init__(self):
        self.blob_info = []
        self.target_info = []
        self.tag_info = []

    def collect(self):
        self.blob_info = []
        self.target_info = []
        self.tag_info = []

        tag_to_blob = {}
        tid_to_tgt = {}
        for i in range(1, 4):
            target_info = {
                'name': None,
                'id':  f'{i}.{i}',
                'node_id': i,
                'rem_cap': 100 * i,
                'max_cap': 1000 * i,
                'bandwidth': 5000 * i / 3,
                'latency': 50 / i,
                'score': 1 / i,
            }
            self.target_info.append(target_info)
            tid_to_tgt[target_info['id']] = target_info
        self.target_info.sort(reverse=True, key=lambda x: x['bandwidth'])
        for i, target in enumerate(self.target_info):
            target['name'] = f'Tier {i}'
        
        for i in range(1, 100):
            blob_info = {
                'name': f'Blob {i}',
                'id': f'{i}.{i + 100}',
                'mdm_node': int(i),
                'tag_id': f'{i}.{i + 500}',
                'score': i / 100,
                'access_frequency': 0,
                'buffer_info': []
            }
            for buf in range(1):
                buf_info = {
                    'target_id': f'{i % 3 + 1}.{i % 3 + 1}',
                    'node_id': 0,
                    'size': 10
                }
                buf_info['node_id'] = tid_to_tgt[buf_info['target_id']]['node_id']
                blob_info['buffer_info'].append(buf_info)
            self.blob_info.append(blob_info)
            if blob_info['tag_id'] not in tag_to_blob:
                tag_to_blob[blob_info['tag_id']] = []
            tag_to_blob[blob_info['tag_id']].append(blob_info['id'])

        
        for i in range(1, 100):
            tag_info = {
                'id': f'{i}.{i + 500}',
                'mdm_node': int(i),
                'name': f'Tag {i}',
                # 'blobs': [self.unique(blob.blob_id) for blob in tag.blobs]
                'blobs': []
            }
            if tag_info['id'] in tag_to_blob:
                tag_info['blobs'] = tag_to_blob[tag_info['id']]
            self.tag_info.append(tag_info)

# mdm = MetadataSnapshot()
# mdm.collect()
# print('Done')
