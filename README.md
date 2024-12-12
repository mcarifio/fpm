# homework

## Summary

The python project `homework` implements the Dependency Resolution Problem stated below. It's not complete. See the Analysis section below.

## Problem: Dependency Resolution Algorithm

_You are tasked with developing a dependency resolver for a Linux package manager. Given a set of packages and their dependencies
represented as a directed graph, design an algorithm to determine the order in which packages should be installed to satisfy all
dependencies, considering cyclic dependencies and ensuring minimal installations. Implement your solution in the language of your
choice._

## Solution(ish)

The solution consists of these python modules and classes:

* pkg.Package: represents a package, it's metadata and in particular it's immediate dependencies, a list of pkg.Packages.

* checker.check(): a function that checks invariant conditions and logs warnings or raises AssertionErrors depending on the
  caller's desire. Used by pkg.Package.conforms().

* graph.Node: represents the directed graph, input to resolver.Resolver.resolve.

* repo.Repo, repo.Everything: the set of all available packages "out there".

* resolver.Resolver: resolves if a set of packages can be installed from repo.Everthing

* dispatcher: grafts a cli onto each module

* client: a cli client that pulls it all together

Note that every python source file *.py should be considered a (self-contained) module. In particular each
module (== file) contains at least one `TestCase` class to drive `pytest` or `unittest`. Likewise, each
module can be invoked at the command line with `-m ${module} ${verb}`. Verbs are per module, but share some
common ones like `about` or `test`.

Not every class or module is complete nor have all implementation questions have been answered.
As per developer convention, I've annotated open questions with `TODO` comments, e.g. `# TODO mike@carif.io: is dispatch by object type too brittle?`.
I've also included some "stage directions" in the comments about what to flesh out next. As Steve Job's said: "Shipping is a feature."
But no program is completely done. Summarizing the current implementation _and_ next steps is my compromise.

I have a personal habit of keeping a `scratch` directory in a project for experiments, for useful data and for ideas I might
revisit later. In this homework context, you might find it a little confusing but ignore it. The naming of the directory --
_scratch_ -- follows a classic math student convention where private noodling is off to the side and isn't part of the proof.

## Project Layout

After you've open `mcarifio-geico-homework.tgz` with (say) `tar xaf mcarifio-geico-homework.tar.gz`, you should see:

```bash
homework ## you are here
├── AUTHORS.md ## python convention
├── checker.py ## checker.check()
├── cli.py ## client.on_main()
├── dispatcher.py ## dispatcher.mkdispatcher(), turns a module into a cli
├── graph.py ## graph.Node
├── pkg.py ## pkg.Package
├── poetry.lock ## locks down python dependencies, suitable for git commit
├── pyproject.toml ## metadata about the homework project, consumable by the python ecosystem, including poetry.
├── README.md ## you are here even more
├── repo.py ## represents a source of packages
├── resolver.py ## resolves graphs of packages for fun and profit
├── scratch ## side experiments
│         ├── data ## experiments with fetching data from official distro repositories, in this case fedora; deferred; NOT IN ARCHIVE
│         │         └── repo
│         │             └── fedora
│         │                 ├── butkis.db.json
│         │                 ├── fedora.repo.json
│         │                 ├── primary.json
│         │                 ├── primary.xml
│         │                 └── repomd.xml
│         ├── mod.py
│         └── semver
│             ├── cli.py
│             ├── __init__.py
│             ├── __main__.py
│             └── Version.py
└── tasks.py

7 directories, 32 files
```

## Walkthrough

This python project uses `pyproject.toml` to describe it's own dependencies and development environment.
It's tightly integrated with `poetry`. Therefore, the "first time" (and one time) setup is:

```bash
python -m pip install -U pip
python -m pip install -U pipx
python -m pipx install poetry
type -P poetry # ~/.local/bin/poetry
poetry --version # 1.8.5 or later
```

Next, establish your development environment:

```bash
git clone https://github.com/mcarifio/homework ~/src/geico/homework && cd ~/src/geico/homework
poetry install
poetry run pkg version
poetry run pkg test
poetry run python -m pkg version
poetry run python -m pip list | grep homework
```

Note this is similar to activating the poetry venv manually with these commands:
```bash
source $(poetry env info --path)/bin/activate # for bash
python -m pip list | grep homework
python -m pkg version
```
`poetry run` just activates and deactivates the venv on your behalf.

Finally, if you live dangerously, you can install `pylint` and `pytest` in your local python 3.13 environment say `--user`. You'll use
them all the time:
```bash
python -c 'import sys; assert sys.version_info.major >= 3; assert system.version_info.minor >= 13'
python -m pip install --user -U pylint pytest
```
Installing these packages (more) globally makes them more convenient and takes poetry and package installing out of the picture. It's one
less moving part, especially initially as you find your "poetry legs".

If you embrace the danger, you can run all the unittests directly with `pytest` or `unittest`:
```bash
pytest *.py ## colorized output
python -m unittest --verbose *.py ## utilitarian
```

## Background (and Some Philosophy)

See `pyproject.toml` for project dependencies, including python 3.13 and development packages (which the walkthrough exercised above).
I used no external python packages in the implementation. In the wild, I would have investigated
[NetworkX](https://networkx.org/) to represent the graph of packages. Python's "batteries included" philosophy makes "just python" possible. So I did that.

Although I did consider where I was going before I started writing code (see the Retrospective section below), I also experimented
with ideas and concepts. Python, with it's Read-Eval-Print loop, is ideal for this. You don't get to see any of that, but it
happened. No. Really.


## Analysis

The resolver implementation is a _recursive_ post order traversal of a graph of packages in dependency order (outgoing nodes)
starting with the root node. Since python does *not* provide tail recursion optimization (by design) and the default
recursion stack is `sys.recursionlimit()` or 1000 stack frames, the traversal functions graph.Node.postorder() and graph.Node.preorder()
depth levels max out 1000. That probably wouldn't be a practical issue, but the traversal methods allow for upping the recursion
limit above this value on a per call basis.

The post order traversal generates a "bottom up" unique list of packages starting with the frontier of the graph (all nodes with no
children) followed by interior nodes. Since versions aren't considered and duplicates are skipped
during traversal, the list is consistent. If and when version specifiers are introduced, the running set of version constraints for each
package are gathered up. They can be evaluated on the fly or after the fact. If they are evaluated during traversal, the traversal can
be short circuited when a constraint is violated. Evaluation afterwards would lead to better error messages (I think) and the resolver
could report multiple violations.

The

Traversal worst case complexity is order(n^2) with the "seen" stack growing order(n).

## Tests

Each module has a TestCase with test methods that exercise that module. The test suite can be invoked with
`python -m ${module} test`. Or you can run all of them with `pytest` or `python -m unittest --verbose *.py`:

```bash
mcarifio@butkis:~/src/geico/homework$ pytest *.py
================================================================= test session starts ==================================================================
platform linux -- Python 3.13.0, pytest-8.3.3, pluggy-1.5.0
rootdir: /home/mcarifio/src/geico/homework
configfile: pyproject.toml
plugins: hypothesis-6.115.6, anyio-4.6.2.post1
collected 23 items

cli.py .                                                                                                                                      [  4%]
graph.py .........                                                                                                                               [ 43%]
pkg.py ........                                                                                                                                  [ 78%]
repo.py ...                                                                                                                                      [ 91%]
resolver.py ..                                                                                                                                   [100%]

================================================================== 23 passed in 0.43s ==================================================================
```

There aren't nearly enough tests and there are no mock objects to test objects with "mockable" endpoints such as `repo.Repo`.


## Retrospective

I wrote the section _Prep and Thinking_ below before I implemented the problem. I've retained it so I can review my
problem solving at some later date. The takeaways:

* After review with the customer (Townsend), versions were deemed unnecessary and outside the scope. They can be added later.
  Nevertheless I stubbed out a Package.Version class for future work.

* I chose json as the serialization for package definitions and the repository of packages. This leaves the door open for
  other formats to describe packages and repositories, using json as the serialization between various parts. Everything (including webbrowers)
  talks json. Other formats such as yaml can be converted into json. Databases such as postgres can traffic in json. Seems like a safer choice.

* As an aside, cookiecutter, which generates python project layouts, saved me nothing. In fact, it got in the way.

* I used the homework assignment as a personal learning vehicle, in particular:

  - I purposely used some of the new python features, specifically the assignment operator `:=`, the `match/case` statement
    and the python `type` statement for type aliasing.

  - I purposely experimented with several Large Language Model (LLM) code generation tools:
    + [chatgpt 4o](https://chat.openai.com/)
    + claude.io
    + Microsoft copilot
    + Google Gemini
    + [perplexity.ai](https://perplexity.ai/)
    + Jetbrain's code plugin for pycharm

The LLM generated code was almost always wrong in the details, but often employed the right tactics and I could fill
in the right details after some reading and experimentation. Pycharm completion based on (their) Large Language Models
is particularly powerful for boilerplate situations and (less often) crafting unit tests.

### Prep and Thinking

_This section, written before I started coding, outlined my initial tactic(s)._

* Sketch out an approach (see below).

* Review dependency resolution "in the literature":
  - `dnf5` and `dnf` (rpm based systems)
  - `apt` (`deb` based systems),
  - python's [pip](https://pip.pypa.io/en/stable/topics/dependency-resolution/)
  - rust's [cargo](https://doc.rust-lang.org/cargo/reference/resolver.html)
  - node's [npm]()

  These systems all resolve dependencies. Hopefully I don't need backtracking otherwise I might write this in prolog (note:
  I didn't need backtracking). Previewing the literature is also a good opportunity to better understand the resolvers in languages I use or want to use.

* Review python classes, modules and directory modules (I periodically reread documentation. Sporadically revisiting
  topics (re)solidifies concepts and I'm about to write a few classes and unit tests.)

* Write the `semver.Version` class plus pytests. I'll probably use "dunder operators" to overload things like comparisons.
  (This was deemed outside the scope. I started `pkg.Version` anyways.)

## (Initial) Approach

Here's how I think the python implementation will go. The literature above might guide me elsewhere; we'll see.

* Invent an easily parsable package definition format say `.pkg.yaml`. It needs to define:
  - the package name (required)
  - the package id that is globally unique, probably a uuid (required but can be automatically generated on behalf of the packager).
    Might not need this for the programming prompt.
  - the package version {major}.{minor}.{patch} (assuming dependency resolution takes version into account)
  - a build id since {patch} might not be granular enough
  - optionally, metadata or backpointers to source repositories or source tars depending on the packager's preference
  - immediate or direct dependencies as a list and a declaration of possible versions allowed for that dependency. These declarations
    are used to "narrow" the allowed set of versions. If a dependency is "narrowed" to the empty set, then the root package can't
    successfully be installed.
  - pre-install and post-install triggers (which I won't implement, but needed for installation "in the wild")

* Invent (or pillage) a package repository structure, probably a file tree served by an https server (deferred to later).

* Invent (or pillage) a handle to each possible repository (deferred).

* Invent (or pillage) a method for traversing all exposed handle's repositories to get the set union of all available packages available for installation.
  Repeats are allowed and multiple handles are retained. A repository could be down during an update so knowing alternatives is fault-tolerant.

Note that I'll wave my hands on the repository building part and represent the set of all versions of all packages in something like `mock.repo.yaml`.
Building a `.repo.yaml` is non-trivial (and why I'm handwaving). The problem description picks up "in the middle" where I've been asked to
install a set of packages. I generate a graph of packages and subpackages top down, left to right from the set of packages initially given, a list of "roots"
as it were. I then traverse this graph "pre-order" to generate a "bottom up(ish)" list with a set of all the version "declarations" "in play" from any
part of the graph. I have to keep a set of visited nodes to avoid loops.

Some package systems (`dnf`, `apt`) run post-install triggers. So I think that means the post-install triggers of dependencies must run first and
all succeed before the parent is run. But if I wave away triggers, does the package order above become irrelevant?

Note that my "design" is basically `apt` or `dnf` without any cryptography, package signing and transactions. If you install dependencies but the
parent package installation fails, you have the detritus of the children (yuck).

Note that so called "immutable" platforms like [Fedora Silverblue](https://fedoraproject.org/atomic-desktops/silverblue/), based on [ostree](https://ostreedev.github.io/ostree/), do not traffic in packages.
They are image based with a "layered" file system (the "git-like" claim).  I'm still wrapping my head around them as I continue to
explore [Fedora Bluefin](https://projectbluefin.io/)

At the end, I hope to have a python cli something like `client.py --repo=all.repo.yaml install pkg0.pkg.yaml[=${version}] pkg1.pkg.yaml ...`.
This might prove to be a little ambitious but a guy's gotta dream.

## TODO

* Installation package order is really graph traversal. If I were to reverse the dependency relationship "arrows" and start with the "frontier" of the
  package graph (all nodes with no dependencies) and traverse toward the "roots", is that the best order?

* Pip does a pretty good job of specifying dependency constraints in terms of versions but I don't want to write a little string parser. How to finesse this?

* `mcarifio-geico-homework.tar.xz` was created with `tar caf mcarifio-geico-homework.tar.xz --exclude=__pycache__
   --exclude=scratch/data --exclude=.pytest_cache --exclude=.idea homework`. Write a `poetry` script for that?

## Credits

The initial project layout was created with cookiecutter and the [briggySmalls/cookiecutter-pypackage](https://github.com/briggySmalls/cookiecutter-pypackage) project template.
Whatever time I thought I would save leveraging someone else's work I probably lost trying to understand it.
