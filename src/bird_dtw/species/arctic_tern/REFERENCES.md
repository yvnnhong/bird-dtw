# Arctic Tern References

## Primary Sources

Egevang, C., Stenhouse, I. J., Phillips, R. A., Petersen, A., Fox, J. W., Silk, J. R. D. (2010).
"Tracking of Arctic terns Sterna paradisaea reveals longest animal migration."
*Proceedings of the National Academy of Sciences*, 107(5), 2078-2081.
https://doi.org/10.1073/pnas.0909493107

Alerstam, T., Bäckman, J., Grönroos, J., et al. (2019).
"Hypotheses and tracking results about the longest migration: The case of the arctic tern."
*Ecology and Evolution*, 9(17), 9511-9531.
https://doi.org/10.1002/ece3.5459
<!-- keep only if params.py actually uses values from this paper -->

## Data

Example/test tracking data (GPS/geolocator fixes) sourced via OBIS-SEAMAP:
https://obis.org/dataset/f3316d34-fbbd-4c9a-9c1b-382a1d9877d3

License: CC-BY-NC 4.0 (non-commercial use only). Data is fetched at runtime
via the OBIS API and is NOT redistributed in this repository.
See `species/arctic_tern/data.py`.

## Key Parameters Used

- Migration speed: Egevang et al. (2010), Table 2
- Stopover duration: Egevang et al. (2010), Table 1
- Route variation: Alerstam et al. (2019), Table 1