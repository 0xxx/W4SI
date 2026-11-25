# Local Zola site

This is a local Zola site using the upstream Ametrine theme.

## Preview and build

```sh
zola serve --interface 127.0.0.1 --port 1111
zola build
zola check --skip-external-links
python3 tests/test_build.py
```

Preview address: <http://127.0.0.1:1111>.

## Verified versions

- Zola: `0.23.6`
- Ametrine: `71b925c30384a42c7e7d3f4da8a5f225697fe772`
- Ametrine icons: `748232862ae847d2f911db82c655c159496a2c56`
- Citrine Sass: `a3b037a48eb521fcc7c2be312c2c2105cfe02a8c`

## Customize

- Set the final website URL in `base_url` in `config.toml`. It currently points to localhost.
- Add your own Git remote when you are ready:

```sh
git remote add origin <their-repository-url>
```

- Edit the homepage in `content/_index.md`, About page in `content/about.md`, and posts under `content/blog/`.
- Navigation, colors, and display options live in `config.toml`.
- The theme is a Git submodule at `themes/ametrine`; its source is <https://codeberg.org/daudix/ametrine>.
