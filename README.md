
# JavaRepoMiner
**JavaRepoMiner** is a python tool which can detect the java method signature after and before a commit. In this repo, JavaRepoMiner mines a given Java GitHub code repository and analyses all the commits in that repository to find the commits that have added a parameter to an existing method. For example, assume that we have a method _test(int x)_ in a Java file. If a commit changes this method to be _test(int x, int y)_ then this commit added a parameter to this function and this project will detect that. 

**JavaRepoMiner** makes a report in CSV file with columns  "Commit SHA, Java File, Old function signature, New function signature”. 

## Getting Started

### Requirements

- Python 3.X
- Git

### Setting up the requirements

* To install git in Linux:
```groovy
sudo apt-get install git
```

* To install **PyDriller**[[1](#references)]:
```groovy
pip install pydriller
```

## Module and Methods

- **RepoMiner.py** This module wil take the Java code repository as input and write the output as described in a CSV file upder the _Outputs_ folder.


-  _RepoMiner_ method takes the git repo name as input and returns the results to write in CSV.


- _isMethod_ method checks the JAVA statements and ensures that statement is a method or not.


## How it works

After running the _RepoMiner.py_ module, it will prompt for input. The input is the JAVA code repository. For example, we have a repo named _JavaTestingRepo_ in parent directory, then input will be like _../JavaTestingRepo_. Then it write the result in this project in a folder name output as _Result.csv_.

## Run
To run the code:
```
$git clone https://github.com/habibrahmanbd/JavaRepoMiner.git
<RepoNameWIthDirectory>
```

## Datasets

Two popular JAVA git repo, _java-design-patterns_ [[2](#references)] and _RxJava_ [[3](#references)] is used as dataset. _JavaTestingRepo_ [[4](#references)] is a demo git repo for running this code while developing.

## Results

- _java-design-patterns.csv_ is the result of [[2](#references)]
- _RxJava_ is the result of [[3](#references)]
- _JavaTestingRepo_ is the result of [[4](#references)]

## References

- [1] https://github.com/ishepard/pydriller

- [2]: https://github.com/iluwatar/java-design-patterns

- [3]: https://github.com/ReactiveX/RxJava

- [4]: https://github.com/habibrahmanbd/JavaTestingRepo

## Acknowledgement:
I would like to thank <a href = "https://sarahnadi.org/" > Sarah Nadi</a>, Assistant Professor in the Department of Computing Science at the University of Alberta for assigning me this coding task.
