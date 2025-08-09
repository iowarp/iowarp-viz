# IoWarp Viz

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![IoWarp](https://img.shields.io/badge/IoWarp-GitHub-blue.svg)](http://github.com/iowarp)
[![GRC](https://img.shields.io/badge/GRC-Website-blue.svg)](https://grc.iit.edu/)
[![Python](https://img.shields.io/badge/Python-3.7+-yellow.svg)](https://www.python.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Flask-green.svg)](https://flask.palletsprojects.com/)

A real-time visualization tool for monitoring and analyzing IOWarp runtime behavior and performance metrics.

## Purpose

IoWarp Viz provides an interactive dashboard for visualizing the behavior of IOWarp as it runs, helping developers and system administrators understand I/O patterns, performance bottlenecks, and system behavior in real-time.

## Tutorial

Tutorial documentation is coming soon. For now, please refer to the installation and usage instructions below.

## Dependencies

### System Requirements
- Python >= 3.7
- IOWarp runtime installed and configured

### Python Dependencies
- `pybind11` - Python/C++ interface bindings
- `pytest` - Testing framework
- `flask` - Web framework for the visualization dashboard

## Installation

### Prerequisites

First, ensure you have the required Python dependencies:

```bash
pip install pybind11 pytest flask
```

#### Build and Install

1. Clone the repository:
```bash
git clone https://github.com/iowarp/iowarp-viz.git
cd iowarp-viz
```

2. Install using pip:
```bash
pip install -e .
```

This will install the `py_hermes_mdm` package and copy the dashboard files to `~/.hermes_viz`.

#### Alternative: Direct Setup

```bash
python setup.py install
```

## Usage

After installation, start the visualization server:

```bash
hermes_viz_server
```

Then open your browser and navigate to the dashboard (typically at `http://localhost:5000`).

## Testing

Run the test suite:

```bash
pytest test/unit/
```

## Project Structure

- `bin/` - Executable scripts
- `dashboard/` - Web dashboard HTML/JS files
- `py_hermes_mdm/` - Python metadata manager interface
- `test/unit/` - Unit tests

## License

BSD 3-Clause License

Copyright (c) 2024, Gnosis Research Center, Illinois Institute of Technology. See the [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue on the [GitHub repository](https://github.com/iowarp/iowarp-viz).
