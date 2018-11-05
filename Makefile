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
