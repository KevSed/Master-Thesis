et: build/thesis.pdf


TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build

build/thesis.pdf: FORCE Plots/hillas.pdf | build
	latexmk $(TeXOptions) thesis.tex
	mv build/thesis.pdf master_thesis_kevin_sedlaczek.pdf

FORCE:

build:
	mkdir -p build/

clean:
	rm -rf build

Plots/hillas.pdf: plot_hillas.py matplotlibrc_column header_matplotlib.tex
	TEXINPUTS=$$(pwd): \
	MATPLOTLIBRC=matplotlibrc_column \
	python plot_hillas.py
