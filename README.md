# Book Embeddings

This README.md file contains basic information about this project and instructions on how to edit and/or and run the project.

## Table of Contents
1. Description

1. Requirements

1. Installation

1. Usage

1. Contributions

1. Sources

1. License

## Description

The files contained in this repository were used to assist in finding $1$-page generalized book embeddings of graphs. The paper for which it assisted is titled "Klein Book Embeddings" which has the following abstract

 >Book embeddings of graphs have been the subject of extensive study. The definitions of such
    embeddings have been generalized by allowing pages to be cylinders, tori, and M\"obius bands rather than half-
    planes. In this paper, we consider book pages as Klein bottles. We give an application of these Klein books
    and edge bounds for graphs embeddable in the books. We conclude with optimal Klein book embeddings
    of some families of graphs.

  This code can search for valid $1$-page embeddings for cylinder, torus, M\"obius, and Klein books across the space of possible vertex spine orderings. Because the number of possible orderings grows at a factorial rate, this code only works well for graphs of 11 vertices or less. Book embeddings are found in a somewhat naive manner, and future work could be done to improve the efficiency of the algorithm. 

## Requirements

This project assumes you have [Python](https://www.python.org/) downloaded and installed on your local machine. Visit the downloads page [here](https://www.python.org/downloads/) to find the latest release for Windows, macOS, or Linux. You can confirm that Python was correctly installed on your machine and is accesible globally by simply running the command `python` or `python3` on any terminal. If you believe Python is installed correctly but that is not working, it is likely that your path variable was not set up correctly. 

## Installation 

Clone this repository to your local machine and navigate to the root of the cloned repository.

## Usage

Once all dependencies are downloaded and installed, you can run the Python scripts with the command `python main.py`.

## Contributions

This project was created and developed by [Luke Martin](https://github.com/lmartin5) as part of a research group in graph theory. The research was conducted Gonzaga University in the 2022-23 academic year.

## Sources

The GeeksForGeeks article ["Python Program to print all permutations of a given string"](https://www.geeksforgeeks.org/python-program-to-print-all-permutations-of-a-given-string/) was vital for generating all possible vertex orderings. 

## License 

This project is licensed under the GNU general public license. See the LICENSE file.