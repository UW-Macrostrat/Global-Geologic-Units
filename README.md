# GeoDeepDive Ignimbrite Application

A test application built by Daven Quinn to subset data about ignimbrites from the GeoDeepDive database.

## Executables

All of the functionality of the model can be accessed from a single
executable.

- `bin/run-model setup` installs required Python packages and install PostGIS extension
- `bin/run-model load-test-data` provisions test data in the
  `ignimbrites_sentences_nlp352` table (optionally specifying a filename)
- `bin/run-model --all` runs the model and dumps generated tables (excluding the
  main sentences table) to the `output` directory.

All of the steps of the model can be run independently, check out
`bin/run-model --help` for details.


Check out [the wiki](https://github.com/UW-Deepdive-Infrastructure/app-template/wiki) for more information on getting started.

## License
CC-BY 4.0 International for application exceuction on GDD infrastructure applied to open access documents 

CC-BY-NC 4.0 International for application exceuction on GDD infrastructure applied to select non-open access documents 
