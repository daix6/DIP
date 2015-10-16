# DIP Homework 1: Fundamentals
## Xuan Dai, 13331043

### 1 Exercises

#### 1.1 Storage

1. How many bit planes are there for this image?
    * $log_2^{256} = 8\ bit\ planes$.

2. Which plane is the most visually significant one?
    * Plane 8, which contains all the highest-order bits.

3. How many bytes are required for storing this image? (Don’t consider image headers and compression.)
    * $2048\*2048\*8\ bits = 2^{22}\ bits$

#### 1.2 Adjacency

1. There is no 4-path between p and q since $N_{4} q = \emptyset$.

2. There is one shortest path between p and q with length 4.

3. There is one shortest path between p and q with length 4.

#### 1.3 Logical Operations

1. $A \cap B \cap C$
2. $(A \cap B) \cup (B \cap C) \cup (A \cap C)$
3. $(\overline{A} \cap B \cap \overline{C}) \cup (A \cap \overline{B} \cap C)$ 
