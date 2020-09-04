# Tutorial

[tutorials.ipynb](https://nbviewer.jupyter.org/github/agy-why/gaia-tap-pyvo-tutorials/blob/master/tutorials.ipynb): [![run it online](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/agy-why/gaia-tap-pyvo-tutorials/master?filepath=tutorials.ipynb)

# Examples 

A few scripts to access data via the TAP interface of gaia.aip.de with pyvo

* [gaia-tutorial-sync.py](gaia-tutorial-sync.py) : submit and retrieve a short query
* [gaia-tutorial-async-30s.py](gaia-tutorial-async-30s.py) : submit and retrieve an asynchrone query to the 30 second queue
* [gaia-tutorial-async-5m.py](gaia-tutorial-async-5m.py) : submit and retrieve an asynchrone query to the 5 minutes queue
* [gaia-tutorial-submit-2h.py](gaia-tutorial-submit-2h.py) : submit an asynchrone query to the 2 hours queue
* [gaia-tutorial-retrieve-2h.py](gaia-tutorial-retrieve-2h.py) : retrieve an asynchrone query from the 2 hours queue
* [gaia-tutorial-submit-multi.py](gaia-tutorial-submit-multi.py) : submit chunked queries
* [gaia-tutorial-retrieve-multi.py](gaia-tutorial-retrieve-multi.py) : retrieve chunked queries
* [gaia-tutorial-from-files.py](gaia-tutorial-from-files.py) : submit and retrieve multiple queries from files
* [gaia-archive-jobs.py](gaia-archive-jobs.py) : archive completed jobs
* [gaia-rerunning-archived-jobs.py](gaia-rerunning-archived-jobs.py) : resubmit and retrieve archived jobs

## Usage

replace the `<your-token>` with your authentification Token for `gaia.aip.de` and run the
scripts as `python <script>.py`.
