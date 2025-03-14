const BACKEND_URL = 'http://localhost:##PORT##';
const BLOBS_URL = `${BACKEND_URL}/api/blobs`;
const TAGS_URL = `${BACKEND_URL}/api/tags`;
const TARGETS_URL = `${BACKEND_URL}/api/targets`;
const ACCESS_PATTERN_URL = `${BACKEND_URL}/api/access_pattern`;

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
setInterval(pollJsonApi(TARGETS_URL), 5000);         // Poll every 5 seconds
setInterval(pollJsonApi(ACCESS_PATTERN_URL), 5000);  // Poll every 5 seconds

async function updateTargetDisplay() {
  const targets = await pollJsonApi(TARGETS_URL);
  const pattern = await pollJsonApi(ACCESS_PATTERN_URL);
  const container =
      document.getElementById('targets-container') || createContainer();
  console.log(pattern);

  container.innerHTML = '';
  targets.forEach(target => {
    const box = document.createElement('div');
    box.className = 'target-box';

    const usage = target.max_cap - target.rem_cap;
    const usagePercent = ((usage / target.max_cap) * 100).toFixed(1);

    box.innerHTML = `
            <h3>${target.name}</h3>
            <p>Free Space: ${formatBytes(target.rem_cap)}</p>
            <p>Used Space: ${formatBytes(usage)}</p>
            <p>Capacity: ${formatBytes(target.max_cap)}</p>
            <p>Usage: ${usagePercent}%</p>
            <p>Net I/O reqs: ${pattern.count}</p>
        `;

    container.appendChild(box);
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