et: build/thesis.pdf


TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build

build/thesis.pdf: FORCE | build
	latexmk $(TeXOptions) thesis.tex
	mv build/thesis.pdf master_thesis_kevin_sedlaczek.pdf

FORCE:

build:
	mkdir -p build/

clean:
	rm -rf build

# Plots/hillas*: plot_hillas.py matplotlibrc header_matplotlib.tex
# 	TEXINPUTS=$$(pwd)/header_matplotlib.tex: \
# 	MATPLOTLIBRC=matplotlibrc \
# 	python plot_hillas.py

# Plots/zenith.pdf: build/runs.csv
# 	TEXINPUTS=/home/kevin/Documents/Master-Thesis/header-matplotlib.tex \
# 	MATPLOTLIBRC=/home/kevin/Documents/Master-Thesis/matplotlibrc_full \
# 	python plot_zenith.py

build/runs.csv: build
	curl -o build/runs.csv https://www.fact-project.org/data/open_crab_sample_runs.csv

eps: eps_scores.pdf eps_sigma.pdf eps_theta_cut.pdf

eps_scores.pdf eps_sigma.pdf eps_theta_cut.pdf:
	TEXINPUTS=$$(pwd): MATPLOTLIBRC=./matplotlibrc_full \
	python plot_eps_scores.py
