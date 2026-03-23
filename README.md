# Value Alignment in Online Shopping Behavior

This project investigates value alignment in online shopping behavior by inferring latent shopper preferences from session-level data and quantifying how consistently actions align with those preferences, especially under contextual shifts. We employ a Bayesian framework using Hamiltonian Monte Carlo (HMC) with the No-U-Turn Sampler (NUTS) to estimate preference parameters, and develop a rationality-based alignment metric.

## Project Structure

```
.
├── _quarto.yml          # Quarto website configuration
├── index.qmd            # Overview page
├── data.qmd             # Data & EDA page
├── transforms.qmd       # Transforms & Preprocessing page
├── model.qmd            # Modeling Framework page
├── alignment.qmd        # Rationality & Alignment page
├── evaluation.qmd       # Evaluation & Robustness page
├── discussion.qmd       # Discussion & Extensions page
├── assets/
│   ├── figures/         # Final figures for publication
│   └── diagrams/        # Lucidchart exports (SVG preferred)
├── notebooks/           # Full analysis notebooks
│   ├── 01_eda.ipynb
│   ├── 02_transforms.ipynb
│   ├── 03_hmc.ipynb
│   └── 04_alignment.ipynb
├── src/                 # Python modules
│   ├── data.py
│   ├── transforms.py
│   ├── model.py
│   ├── alignment.py
│   └── evaluation.py
└── docs/                # Generated website (GitHub Pages output)
```

## Installation

### Install Quarto

1. **macOS**: 
   ```bash
   brew install quarto
   ```

2. **Linux/Windows**: Download from [quarto.org](https://quarto.org/docs/get-started/)

3. Verify installation:
   ```bash
   quarto --version
   ```

### Python Dependencies

Install required Python packages:

```bash
pip install pandas numpy scikit-learn pymc arviz matplotlib seaborn
```

## Local Development

### Preview Website Locally

To preview the website locally with live reload:

```bash
quarto preview
```

This will start a local server (typically at `http://localhost:4200`) and automatically reload when you make changes to `.qmd` files.

### Render Website

To render the complete website:

```bash
quarto render
```

This generates the static HTML files in the `docs/` directory.

## GitHub Pages Deployment

The website is configured to deploy from the `/docs` directory.

### Setup Instructions

1. **Push your repository to GitHub**

2. **Configure GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under **Source**, select:
     - **Branch**: `main` (or your default branch)
     - **Folder**: `/docs`
   - Click **Save**

3. **Deploy**:
   - After pushing changes, run `quarto render` locally
   - Commit and push the `docs/` directory
   - GitHub Pages will automatically deploy your site
   - Your site will be available at: `https://<username>.github.io/<repository-name>/`

### Automated Deployment (Optional)

You can set up GitHub Actions to automatically render and deploy on push. Create `.github/workflows/quarto.yml`:

```yaml
name: Render Quarto

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: quarto-dev/quarto-actions/setup@v2
      - name: Render
        run: quarto render
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

## Asset Management

### Diagrams

- **Location**: `assets/diagrams/`
- **Format**: SVG preferred (better scaling, smaller file size)
- **Source**: Export from Lucidchart as SVG
- **Placeholder files**: Currently contain placeholder SVGs that should be replaced with actual Lucidchart exports

### Figures

- **Location**: `assets/figures/`
- **Format**: PNG, SVG, or PDF
- **Usage**: Reference in `.qmd` files using:
  ```markdown
  ![Figure caption](assets/figures/figure_name.png)
  ```

## Code Organization

### Notebooks

Full analysis notebooks are in `notebooks/`:
- `01_eda.ipynb`: Exploratory data analysis
- `02_transforms.ipynb`: Feature engineering and preprocessing
- `03_hmc.ipynb`: Bayesian modeling with PyMC
- `04_alignment.ipynb`: Rationality estimation and alignment scores

### Python Modules

Reusable code is organized in `src/`:
- `data.py`: Data loading and validation
- `transforms.py`: Feature transformations
- `model.py`: PyMC model definitions
- `alignment.py`: Rationality and alignment computations
- `evaluation.py`: Evaluation metrics and robustness checks

## Development Workflow

1. **Edit content**: Modify `.qmd` files in the root directory
2. **Preview**: Run `quarto preview` to see changes live
3. **Render**: Run `quarto render` to generate final HTML
4. **Commit**: Commit both source `.qmd` files and generated `docs/` directory
5. **Push**: Push to GitHub to trigger Pages deployment

## Troubleshooting

### Quarto not found

- Ensure Quarto is installed and in your PATH
- Try `which quarto` to verify installation location

### Missing dependencies

- Install Python packages: `pip install -r requirements.txt` (if you create one)
- Ensure Python is accessible: `which python` or `which python3`

### Rendering errors

- Check for syntax errors in `.qmd` files
- Verify all referenced files exist (diagrams, figures, notebooks)
- Check Quarto logs for specific error messages

## License

[Add your license here]

## Author

Nalin Joshi — UC San Diego

