##### overview

We needed a way to flexibly and conveniently see if we have an ebook for a given monograph.

This application allows a lookup to be done on:

- title
- title and author
- callnumber

...and returns either brief results with just the found title and author and url, or fuller results that also display publication-date and language.

Example urls (access may be limited in the future):

- brief:
    - title: <https://library.brown.edu/ebook_finder/api/v1/brief?title=zen>
    - title & author: <https://library.brown.edu/ebook_finder/api/v1/brief?title=zen&author=austin>
    - callnumber 'BQ9288 .A966 2014': <https://library.brown.edu/ebook_finder/api/v1/brief?callnumber=BQ9288%20.A966%202014>

- full:
    - title: <https://library.brown.edu/ebook_finder/api/v1/full?title=zen>
    - title & author: <https://library.brown.edu/ebook_finder/api/v1/full?title=zen&author=austin>
    - callnumber 'BQ9288 .A966 2014': <https://library.brown.edu/ebook_finder/api/v1/full?callnumber=BQ9288%20.A966%202014>

---
