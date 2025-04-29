.PHONY: clean cleanwpdf open

open: report.pdf
	open report.pdf

report.pdf: report.tex (3)content.tex (2)title.tex
	pdflatex --shell-escape $<
	biber $(patsubst %.tex,%,$(<))
	pdflatex --shell-escape $<
	pdflatex --shell-escape $<

clean:
	rm -f *.out *.toc *.aux *.log *.bbl *.blg *.bcf *.xml

cleanwpdf: clean
	rm -f *.pdf
