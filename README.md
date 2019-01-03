# monthly_cloc
Count lines of code in a project over time

## Dependencies

 * cloc ([Count lines of code](https://github.com/AlDanial/cloc/))
 * git ([installation](https://git-scm.com/downloads))

## Usage
`python monthly_cloc.py <date YYYY-mm-dd> <month_count> [git_branch]`

### Example
```
> python monthly_cloc.py 2018-10-01 4
...
Date, Bourne, C++, C/C++, CMake, DOS, Groovy, HTML, JSON, Java, Lua, Markdown, Perl, Prolog, Python, R, Windows, XML, YAML, make, SUM:
2018-10-01, 22, 209377, 13743, 1247, 2, 171, 107, 1063510, 1953, 4263, 7138, 38, 15, 1875, 15, 2, 104, 190, 838, 1327516
2018-11-01, 22, 209483, 14163, 1252, 2, 171, 107, 1071823, 1956, 4271, 7383, 38, 15, 2596, 15, 2, 104, 192, 839, 1337681
2019-12-01, 22, 213857, 14665, 1525, 2, 171, 107, 1134535, 1956, 4293, 7818, 38, 15, 2617, 15, 2, 104, 187, 857, 1407897
2019-01-01, 22, 213679, 14642, 1543, 2, 171, 107, 1134330, 1956, 4293, 7818, 38, 15, 2617, 15, 2, 104, 187, 857, 1407504
```
