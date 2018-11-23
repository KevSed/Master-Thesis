et: build/thesis.pdf


TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build

build/thesis.pdf: FORCE Plots/hillas* | build
	latexmk $(TeXOptions) thesis.tex
	mv build/thesis.pdf master_thesis_kevin_sedlaczek.pdf

FORCE:

build:
	mkdir -p build/

clean:
	rm -rf build

Plots/hillas*: plot_hillas.py matplotlibrc header_matplotlib.tex
	TEXINPUTS=$$(pwd): \
	MATPLOTLIBRC=matplotlibrc \
	python plot_hillas.py
