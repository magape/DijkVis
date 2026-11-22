# Vizualizarea algoritmului lui Dijkstra (DijkVis)

## Română

DijkVis este o aplicație educațională realizată în Python și Tkinter pentru vizualizarea pas cu pas a algoritmului lui Dijkstra.

Aplicația permite introducerea unui graf ponderat, executarea algoritmului și analizarea fiecărei etape a calculului drumurilor minime prin intermediul unei reprezentări grafice și al unor explicații detaliate.

## Funcționalități

- introducerea textuală a unui graf ponderat;
- alegerea nodului sursă;
- executarea algoritmului lui Dijkstra;
- navigarea înainte și înapoi între pașii execuției;
- afișarea distanțelor minime curente;
- evidențierea nodului curent și a muchiilor active;
- evidențierea arborelui drumurilor minime;
- explicații detaliate pentru fiecare operație de relaxare;
- legendă pentru interpretarea elementelor grafice;
- validarea datelor introduse și raportarea erorilor.

## Structura proiectului

```text
DijkVis/
│
├── src/
│   ├── app.py
│   ├── dijkstra.py
│   ├── graph.py
│   ├── layout.py
│   ├── main.py
│   ├── parser.py
│   ├── renderer.py
│   ├── style.py
│   └── transform.py
│
├── tests/
│
├── docs/
│
├── README.md
├── LICENSE
└── .gitignore
```

## Cerințe

- Python 3.11 sau o versiune mai nouă
- Tkinter (inclus în distribuția standard Python)

## Rulare

```bash
cd src
python main.py
```

## Testare

Proiectul conține teste automate pentru principalele module:

```bash
pytest
```

## Documentație

Documentația completă a proiectului este disponibilă în directorul:

```text
docs/
```

Document principal:

```text
docs/DijkVis_MihaiAgape.pdf
```

## Scop educațional

Aplicația a fost dezvoltată pentru studierea algoritmului lui Dijkstra și pentru ilustrarea unor concepte precum:

- grafuri ponderate;
- liste de adiacență;
- distanțe minime;
- relaxarea muchiilor;
- arbori ai drumurilor minime;
- programare modulară;
- interfețe grafice cu Tkinter.

## Licență

Acest proiect este distribuit sub licența MIT.

Consultați fișierul:

```text
LICENSE
```

---

# Dijkstra Algorithm Visualisation (DijkVis)

## English

DijkVis is an educational application built with Python and Tkinter for step-by-step visualisation of Dijkstra's shortest-path algorithm.

The application allows the user to define a weighted graph, execute the algorithm and explore each computation step using graphical visualisation and detailed explanations.

## Features

- textual weighted graph input;
- source node selection;
- Dijkstra algorithm execution;
- step-by-step navigation;
- display of current shortest distances;
- highlighting of the current node and active edges;
- shortest-path tree visualisation;
- detailed explanations for each edge relaxation;
- visual legend;
- input validation and error reporting.

## Project Structure

```text
DijkVis/
│
├── src/
│   ├── app.py
│   ├── dijkstra.py
│   ├── graph.py
│   ├── layout.py
│   ├── main.py
│   ├── parser.py
│   ├── renderer.py
│   ├── style.py
│   └── transform.py
│
├── tests/
│
├── docs/
│
├── README.md
├── LICENSE
└── .gitignore
```

## Requirements

- Python 3.11 or newer
- Tkinter (included with standard Python)

## Running

```bash
cd src
python main.py
```

## Testing

Automated tests are available for the main modules:

```bash
pytest
```

## Documentation

Complete project documentation is available in:

```text
docs/
```

Main document:

```text
docs/DijkVis_MihaiAgape.pdf
```

## Educational Purpose

The application was developed as an educational tool for learning:

- weighted graphs;
- adjacency lists;
- shortest paths;
- edge relaxation;
- shortest-path trees;
- modular programming;
- graphical user interfaces with Tkinter.

## License

This project is released under the MIT License.

See the:

```text
LICENSE
```

file for details.