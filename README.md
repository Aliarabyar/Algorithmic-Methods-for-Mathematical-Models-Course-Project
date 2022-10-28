# Algorithmic-Methods-for-Mathematical-Models
# Course-Project
OPL-CPLEX - Python - Heuristics and Meta-heuristics algorithms

**Problem statement**

In order to develop a shape recognition program, a surveillance company uses a surveillance system consists of a camera, which can take pictures, and a distance sensor which provides auxiliary information. The goal of this system is to determine if a specific shape appears in it. In other words, this system matches a particular pattern in an Image.
- We have an image is modelled with an undirected graph $G=(V ; E)$, where each vertex $v \in V$ is a point (pixel) in the image and $E \subseteq V \times V$.
- An edge $\{u, v\} \in E$ is placed between points $u$ and $v$ according to an edge detection algorithm.
- Arcs $\mathrm{E}$ are weighted using the $\omega: E \rightarrow(0,1)$ such that $\omega(u, v)$ is the Euclidean distance between points $\mathrm{u}$ and $\mathrm{v}$ as measured with the distance sensor and distances are scaled so that they are always less than 1.
- The shape is also modelled with a weighted undirected graph $H=(W ; F)$, where $F \subseteq W \times W$ with weight function $\rho: F \rightarrow(0,1)$.
- A shape $H=(W ; F)$ occurs in an image $G=(V ; E)$ when there is an injective function $f: W \rightarrow V$ (called the embedding of $\mathrm{H}$ in $\mathrm{G}$ ) that is edge-preserving: We consider $\{x, y\}$ is an edge in $H$ if and only if $\{(f(x), f(x))\}$ is an edge in $G$.
- In order to eliminate spurious cases, we are particularly interested in the embeddings that minimize the sum of absolute differences between the weight of an edge e and the weight of $f(e)$.

The goal of this project is, given an image and a shape, to find an optimal embedding according to criterion above.
