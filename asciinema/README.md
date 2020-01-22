This directory includes the configuration for rendering the asciinema
panel in the tekton.dev homepage.

A rendered panel (an asciinema cast) has been included at
`../static/asciinema/demo.cast`. To rebuild the cast, run the commands below:

```bash
./run.sh
rm -f ../static/asciinema/demo.cast
mv ./demo.cast ../static/asciinema/demo.cast
```
