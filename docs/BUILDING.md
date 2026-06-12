# Building the PDF

`notes/ram_model.md` is the canonical source. This document explains how to produce `build/ram_model.pdf` from it.

## Prerequisites

```bash
brew install pandoc
brew install --cask basictex     # ~100MB; .pkg installer needs sudo
sudo installer -pkg /opt/homebrew/Caskroom/basictex/*/mactex-basictex-*.pkg -target /
eval "$(/usr/libexec/path_helper)"   # picks up tlmgr in current shell
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended koma-script eisvogel \
  pgf adjustbox babel-english background bidi csquotes everypage \
  filehook footmisc footnotebackref framed fvextra letltxmacro \
  ly1 mdframed mweights needspace pagecolor sourcecodepro sourcesanspro \
  titling ucharcat ulem unicode-math upquote xecjk xurl zref
```

Confirm everything is in place:

```bash
which pandoc xelatex tlmgr
pandoc --version | head -1
xelatex --version | head -1
```

## Building

```bash
make pdf       # build build/ram_model.pdf
make tex       # build build/ram_model.tex (for LaTeX hackers)
make watch     # rebuild on every save (needs `brew install fswatch`)
make clean     # remove all generated artifacts
make help      # list all targets
```

## Editing workflow

| You want to… | Do this |
|---|---|
| Fix a typo or rephrase prose | Edit `notes/ram_model.md`, run `make pdf`, commit both `.md` and `.pdf` |
| Tweak math formulas | Edit `notes/ram_model.md` using LaTeX syntax (`$inline$`, `$$display$$`), rebuild |
| Adjust page layout / theorem styles | Edit the YAML frontmatter of `notes/ram_model.md` (header-includes block) |
| Hand-tune typography (page breaks, custom envs) | `make tex`, edit `build/ram_model.tex`, run `xelatex build/ram_model.tex` directly |
| Switch fonts | Edit `mainfont`, `mathfont`, `monofont` in the YAML frontmatter |

**Important:** `notes/ram_model.md` is the source of truth. If you hand-edit `build/ram_model.tex` it will be overwritten the next time someone runs `make tex`. Either upstream LaTeX changes back into the markdown, or maintain a separate fork of the `.tex`.

## Math syntax cheatsheet

| Want to write… | Use |
|---|---|
| Inline expression | `$T(n) = O(n \log n)$` |
| Display equation | `$$T(n) = 2T(n/2) + \Theta(n)$$` |
| Greek letters | `\Theta`, `\Omega`, `\Sigma`, `\varphi`, `\gamma`, `\varepsilon` |
| Sums / integrals | `\sum_{i=1}^{n}`, `\int_1^n` |
| Fractions | `\frac{n(n+1)}{2}` |
| Powers / subscripts | `n^2`, `n^{k+1}`, `c_1`, `n_0` |
| Brackets | `\lceil \log_2 n \rceil`, `\lfloor n/2 \rfloor` |
| Square root | `\sqrt{n}` |
| Comparison | `\le`, `\ge`, `\ne`, `\approx` |
| Centered cases | `\begin{cases} 1 & \text{if A} \\ 0 & \text{else} \end{cases}` |
| Aligned multi-line | `\begin{aligned} a &= b \\ &= c \end{aligned}` |

## Troubleshooting

**Font errors** ("Font 'TeX Gyre Pagella' not found"):
- Either install the TeX Gyre fonts (`sudo tlmgr install tex-gyre tex-gyre-math`) or change `mainfont` in the YAML frontmatter to `"Latin Modern Roman"` (always available).

**Eisvogel template not found**:
- The template is vendored at `templates/eisvogel.latex`. Verify it exists. If missing, re-download from `https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.zip`.

**Wide table overflows the page**:
- Add `\small` LaTeX wrapping in the markdown around the table:
  ```
  \begin{small}

  | wide | table |

  \end{small}
  ```

**Pseudocode highlights as a real language**:
- Tag the fence as ` ```text ` not ` ```python ` (no syntax highlighter applies).

**`Overfull \hbox` warnings**:
- Usually harmless — verify the PDF visually. Persistent overflows may need `\sloppy` in the header-includes block.

## Slides (Beamer)

`notes/slides/ram_model_part{1..5}.md` build to one Beamer deck per Part of the main notes, using the metropolis theme. The article PDF (`build/ram_model.pdf`) is unaffected — slide sources live in a sub-directory that `make all` does not glob.

### Extra prerequisites

The metropolis theme is not part of basictex. Install it once:

```bash
sudo tlmgr install beamertheme-metropolis pgfopts
# Only if you remove `mainfont:` from the slide YAML and want metropolis's
# default Fira Sans look:
sudo tlmgr install fira fontaxes
```

Verify the theme is installed:

```bash
kpsewhich beamerthememetropolis.sty   # non-empty path = installed
```

### Building slide decks

```bash
make slides                          # build all decks (build/slides_ram_part1.pdf … part5.pdf)
make build/slides_ram_part1.pdf      # build a single deck
make build/slides_ram_part2.tex      # standalone .tex for debugging
make slides-clean                    # remove slide PDFs only (leaves ram_model.pdf alone)
```

### Authoring conventions

- Slide files start at H2 (`## n. Title`) — no H1.
- `## n. Title` = section divider; `### n.m Title` = one frame (driven by `--slide-level=3` in the Makefile).
- If a frame overflows, either split (`### Title (1/2)`, `### Title (2/2)`) or tag the heading with `{.allowframebreaks}`.
- Two-column layouts use pandoc fenced divs:
  ```markdown
  :::::: {.columns}
  ::: {.column width="55%"}
  …
  :::
  ::: {.column width="45%"}
  …
  :::
  ::::::
  ```
- Math syntax is identical to the article (`$...$`, `$$...$$`, `\begin{aligned}`, `\begin{cases}`, `\boxed{...}`).
- Do **not** set `colorlinks: true` in the slide YAML — it conflicts with metropolis's link styling.

### If metropolis silently falls back to default Beamer

You'll see the blue navigation bar and small frame titles instead of the dark progress bar + large sans serif. Re-run the `tlmgr install` line above, then rebuild.
