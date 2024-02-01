# Find a feasible route utilizing Nearest Neightboor, Simulated Anealing and some Heurístics for FLL competitions.

### This project is carried out with the assistance of the Delta team from São João Nepomuceno

## The algoritm tries to optmize 3 targets variables

- Complexity of a run(as the number of missions in a run increases, the complexity of constructing the tools for that run also grows)
- Time of a run
- Punctuation of a run

## Nearest Neightboor

The start route(starting point for SA optimization) is generated using nearest neightboor heuristic, which consists in select the nearest mission based on current position

## Simulated Anealing

Simulated Annealing is a probabilistic optimization algorithm inspired by the annealing process in metallurgy. The annealing process involves heating a material to a high temperature and then gradually cooling it to remove defects and optimize its structure. Similarly, simulated annealing is used to find an approximate solution to an optimization problem by exploring the solution space and accepting occasional suboptimal moves to escape local minima.

- Initialization: Start with an initial solution to the optimization problem. This could be generated randomly or through some heuristic.

- Temperature Control: Simulated annealing maintains a temperature parameter that controls the likelihood of accepting worse solutions. The temperature is initially set high and is gradually reduced over time. At higher temperatures, the algorithm is more likely to accept worse solutions, allowing for exploration of the solution space.

- Neighborhood Search: At each iteration, a neighboring solution is generated. The neighborhood can be defined in various ways depending on the problem. It might involve small changes or perturbations to the current solution.

- Evaluation: The quality of the new solution is evaluated using an objective function. If the new solution is better than the current one, it is accepted. If it is worse, the algorithm may still accept it with a certain probability determined by the temperature and the extent of the degradation in solution quality.

- Temperature Annealing: The temperature is reduced gradually according to a predefined schedule. As the temperature decreases, the algorithm becomes less tolerant of worse solutions, shifting its focus towards exploitation rather than exploration.

- Termination: The process continues until a termination criterion is met, such as reaching a target temperature or a maximum number of iterations.

I plan to improve the project in the future by enhancing the heuristics and optimizing code performance/quality throughout the seasons. It's worth noting that the code is protected under the GPL (GNU General Public License), and the terms can be found at  [GPL](https://www.gnu.org/licenses/gpl-3.0.en.html)