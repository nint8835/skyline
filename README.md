# Skyline

Skyline is a web app for generating models of GitHub contribution activity, similar to GitHub's now-dead [GitHub Skyline](https://skyline.github.com/) service. It differs in behaviour in a couple of ways, to make it work for my usage better.

# Differences from GitHub Skyline

## Absolute heights instead of relative

GitHub Skyline service behaved the same as their profile contribution graph - the day of the year with the most activity is the brightest shade of green / the tallest tower, with the remainder of days being scaled relative to that. This makes sense for a 2D graph of activity where you only can adjust the colour so much, but for a 3D graph where you can place years side-by-side it makes it hard to compare the activities of different years.

Skyline instead uses absolute heights, with each contribution adding a set height to the column for that day.

## Reduced padding for easier tiling

GitHub Skyline had a large base on each model, which provided a convenient place to display the year and username. However, this made it difficult to display large numbers of years side-by-side.

Skyline forgoes the large base, just adding an extra 2mm of height to each day of the year to enable days with zero activity to be visible. It also aligns the first and last day of each year so that years can cleanly flow into eachother.
