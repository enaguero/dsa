PANDOC   ?= pandoc
TEMPLATE := templates/eisvogel.latex
NOTES    := notes
BUILD    := build

# xelatex on macOS uses CoreText for system font lookup and ignores fonts inside
# the texlive tree unless OSFONTDIR points there. Without this, YAML font picks
# like "TeX Gyre Pagella" fail with `fontspec Error: font cannot be found`.
TEXLIVE_FONTS := $(firstword $(wildcard /usr/local/texlive/*/texmf-dist/fonts/opentype/public))
export OSFONTDIR := $(TEXLIVE_FONTS)//

SRCS := $(wildcard $(NOTES)/*.md)
PDFS := $(patsubst $(NOTES)/%.md,$(BUILD)/%.pdf,$(SRCS))
TEXS := $(patsubst $(NOTES)/%.md,$(BUILD)/%.tex,$(SRCS))

# Default note for `make pdf` / `make tex` / `make watch` (override: make pdf SRC=cheatsheet)
SRC ?= ram_model
PDF := $(BUILD)/$(SRC).pdf
TEX := $(BUILD)/$(SRC).tex
ESSENTIALS_PDF := $(BUILD)/$(SRC)_essentials.pdf
ADVANCED_FILTER := templates/strip-advanced.lua

# --resource-path lets image refs in notes/*.md be written relative to the
# note file (figures/foo.png), which is what GitHub's renderer expects, while
# pandoc runs from the repo root.
PANDOC_FLAGS := \
  --template=$(TEMPLATE) \
  --pdf-engine=xelatex \
  --syntax-highlighting=tango \
  --top-level-division=section \
  --number-sections \
  --resource-path=.:$(NOTES) \
  --toc

# --- Beamer slides ---
# Slide sources live under notes/slides/ so the top-level wildcard in SRCS
# (line 12) doesn't pick them up and `make all` keeps building article PDFs only.
SLIDES_DIR  := $(NOTES)/slides
SLIDES_SRCS := $(wildcard $(SLIDES_DIR)/ram_model_part*.md)
SLIDES_PDFS := $(patsubst $(SLIDES_DIR)/ram_model_part%.md,$(BUILD)/slides_ram_part%.pdf,$(SLIDES_SRCS))

PANDOC_BEAMER_FLAGS := \
  -t beamer \
  --pdf-engine=xelatex \
  --syntax-highlighting=tango \
  --slide-level=3

.PHONY: all pdf tex essentials clean watch help list progress regen review slides slides-clean figures

help:
	@echo "Targets:"
	@echo "  make all                   - build PDFs for every note in $(NOTES)/"
	@echo "  make pdf                   - build $(PDF) from $(NOTES)/$(SRC).md (full reference)"
	@echo "  make essentials            - build $(ESSENTIALS_PDF), stripping advanced sections"
	@echo "  make tex                   - build $(TEX) from $(NOTES)/$(SRC).md"
	@echo "  make $(BUILD)/<name>.pdf $(if $(BUILD), )- build a specific PDF (e.g. make $(BUILD)/cheatsheet.pdf)"
	@echo "  make watch                 - rebuild $(PDF) on every save of $(NOTES)/$(SRC).md (needs fswatch)"
	@echo "  make list                  - list all buildable markdown sources"
	@echo "  make clean                 - remove the $(BUILD)/ directory"
	@echo "  make progress              - update readme.md progress line from problem statuses"
	@echo "  make regen                 - re-fetch LeetCode signatures for all stubs (network)"
	@echo "  make review                - list solved problems by oldest Last-Reviewed (spaced rep)"
	@echo "  make figures               - regenerate notes/figures/*.png from scripts/figures/ (needs uv)"
	@echo "  make slides                - build all beamer decks (build/slides_ram_part*.pdf)"
	@echo "  make $(BUILD)/slides_ram_part1.pdf - build a single deck (1-5)"
	@echo "  make slides-clean          - remove only the slide PDFs"
	@echo ""
	@echo "Override the default source:  make pdf SRC=cheatsheet"

list:
	@echo "Sources: $(SRCS)"
	@echo "PDFs:    $(PDFS)"

all: $(PDFS)

pdf: $(PDF)
tex: $(TEX)
essentials: $(ESSENTIALS_PDF)

$(BUILD):
	@mkdir -p $(BUILD)

$(BUILD)/%.pdf: $(NOTES)/%.md $(TEMPLATE) | $(BUILD)
	$(PANDOC) $< -o $@ $(PANDOC_FLAGS)

$(BUILD)/%.tex: $(NOTES)/%.md $(TEMPLATE) | $(BUILD)
	$(PANDOC) $< -o $@ --standalone $(PANDOC_FLAGS)

# Two-track build: applying templates/strip-advanced.lua drops every fenced
# div tagged `::: {.advanced}` ... `:::`, leaving an essentials-only subset.
$(BUILD)/%_essentials.pdf: $(NOTES)/%.md $(TEMPLATE) $(ADVANCED_FILTER) | $(BUILD)
	$(PANDOC) $< -o $@ $(PANDOC_FLAGS) --lua-filter=$(ADVANCED_FILTER)

slides: $(SLIDES_PDFS)

slides-clean:
	rm -f $(BUILD)/slides_ram_part*.pdf $(BUILD)/slides_ram_part*.tex

$(BUILD)/slides_ram_part%.pdf: $(SLIDES_DIR)/ram_model_part%.md | $(BUILD)
	$(PANDOC) $< -o $@ $(PANDOC_BEAMER_FLAGS)

$(BUILD)/slides_ram_part%.tex: $(SLIDES_DIR)/ram_model_part%.md | $(BUILD)
	$(PANDOC) $< -o $@ --standalone $(PANDOC_BEAMER_FLAGS)

clean:
	rm -rf $(BUILD)

watch:
	@command -v fswatch >/dev/null 2>&1 || { echo "fswatch not installed. brew install fswatch"; exit 1; }
	fswatch -o $(NOTES)/$(SRC).md | xargs -n1 -I{} $(MAKE) $(PDF)

progress:
	@python3 scripts/progress.py

regen:
	@python3 scripts/regenerate_stubs.py

review:
	@python3 scripts/review.py

# Figures are committed; rerun only when a scripts/figures/fig_*.py changes.
figures:
	@command -v uv >/dev/null 2>&1 || { echo "uv not installed. brew install uv"; exit 1; }
	uv run --with matplotlib python scripts/figures/generate_all.py
