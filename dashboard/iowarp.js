const BACKEND_URL = 'http://localhost:##PORT##';
const BLOBS_URL = `${BACKEND_URL}/api/blobs`;
const TAGS_URL = `${BACKEND_URL}/api/tags`;
const TARGETS_URL = `${BACKEND_URL}/api/targets`;
const ACCESS_PATTERN_URL = `${BACKEND_URL}/api/access_pattern`;
const SET_FILTER_URL = `${BACKEND_URL}/api/filters`;
const REFRESH_MS = ##REFRESH_MS##;

async function pollJsonApi(URL) {
  try {
    const response = await fetch(URL);
    const targets = await response.json();
    return targets;
  } catch (error) {
    console.error('Error polling targets:', error);
    return [];
  }
}
setInterval(pollJsonApi(TARGETS_URL), REFRESH_MS);

async function updateTargetDisplay() {
  const targets = await pollJsonApi(TARGETS_URL);
  const container =
      document.getElementById('targets-container') || createContainer();

  // console.log('REFRESH_MS:', REFRESH_MS);
  // console.log('Targets:', targets);
  const targetsMap = new Map();
  targets.forEach(target => {
    if (!targetsMap.has(target.node_id)) {
      targetsMap.set(target.node_id, []);
    }
    targetsMap.get(target.node_id).push(target);
    console.log(target.name);
  });

  container.innerHTML = '';
  const nodeContainer = document.createElement('div');
  nodeContainer.style.display = 'flex';
  nodeContainer.style.flexWrap = 'wrap';
  nodeContainer.style.gap = '20px';
  container.appendChild(nodeContainer);

  targetsMap.forEach((nodeTargets, nodeId) => {
    const nodeDiv = document.createElement('div');
    nodeDiv.className = 'node-container';
    nodeDiv.style.flex = '0 1 auto';
    nodeDiv.innerHTML = `<h2>Node ${nodeId}</h2>`;

    nodeTargets.forEach(target => {
      console.log(target.name);
      const box = document.createElement('div');
      box.className = 'target-box';

      const usage = target.max_cap - target.rem_cap;
      const usagePercent = ((usage / target.max_cap) * 100).toFixed(1);
      const bandwidth = (target.bandwidth * 1000).toFixed(1);
      const latency = (target.latency / 1000).toFixed(1);

      box.innerHTML = `
        <h3>${target.name}</h3>
        <p>Free Space: ${formatBytes(target.rem_cap)}</p>
        <p>Used Space: ${formatBytes(usage)}</p>
        <p>Capacity: ${formatBytes(target.max_cap)}</p>
        <p>Usage: ${usagePercent}%</p>
        <p>Bandwidth: ${bandwidth} MBps</p>
        <p>Latency: ${latency} us</p>
      `;

      nodeDiv.appendChild(box);
    });

    nodeContainer.appendChild(nodeDiv);
  });
}

function createContainer() {
  const container = document.createElement('div');
  container.id = 'targets-container';
  document.body.appendChild(container);
  return container;
}

function formatBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  return `${size.toFixed(2)} ${units[unitIndex]}`;
}

setInterval(updateTargetDisplay, 5000);
updateTargetDisplay();

document.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    const filters = {
      tags_filter: document.getElementById('tags-filter').value,
      max_tags: document.getElementById('max-tags').value,
      blobs_filter: document.getElementById('blobs-filter').value,
      max_blobs: document.getElementById('max-blobs').value,
      nodes_filter: document.getElementById('nodes-filter').value,
      max_nodes: document.getElementById('max-nodes').value
    };

    fetch(SET_FILTER_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(filters)
    }).catch(error => console.error('Error setting filters:', error));
  }
});